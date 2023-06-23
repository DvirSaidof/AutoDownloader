import logging
import webbrowser
import time
from db.redis import RedisClient
from subtitles_api.subtitles import Subtitles, SubtitlesNotFoundException, DestinationFolderNotFoundException
from flask import Flask, render_template, request, redirect, url_for
from piratebay_api.pages.piratebay_page import SearchTorrentPirateBay
from piratebay_api.parsers.piratebay_torrent import PirateBayFilmTorrent


app = Flask(__name__)


class AutoDownloadGUI:
    """
    The AutoDownloadApp interacts with the user/google doc files and receive a file_name to download.
    It will then perform a search query on PirateBay using SearchTorrentPirateBay Class, and download the best result
    (E.G torrent with most seeders).
    Download the torrent using webbroswer module to open UTorrent.
    Download subtitles with Subtitles Class which gets language preferences
    Place all files in a shared folder on a local or remote machine.
    """

    MAX_NUM_OF_TORRENTS = 20
    SLEEP_TIME_AFTER_DL_START = 30
    GOOGLE_SHEET_UI_SLEEP = 3

    def __init__(self, opensubtitles_key: str, language_preferences: str, download_folder: str, logs_folder: str,
                 system_os="linux"):

        self._set_folders(system_os, download_folder, logs_folder)

        self.opensubtitles_key = opensubtitles_key
        self.language_preferences = language_preferences

        self.film_name = None
        self.torrent_selected = None
        self.torrents_options = dict()
        self.torrents = []

        self.redis_client = RedisClient(host='localhost', port=6379)

        download_log = "auto_download_app.log"
        logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%d-%m-%Y:%H:%M:%S',
                            level=logging.DEBUG,
                            filename=f'{self.logs_folder}{self.path_divider}{download_log}')

        logging.FileHandler(f'{self.logs_folder}{self.path_divider}{download_log}', 'w', 'utf-8')
        self.logger = logging.getLogger("gui")

    def _set_folders(self, system_os, download_folder, logs_folder):

        linux_divider = "/"
        windows_divider = "\\"
        self.path_divider = ""

        if system_os == "windows":
            self.path_divider = windows_divider
            if linux_divider in download_folder:
                download_folder.replace(linux_divider, self.path_divider)
            if linux_divider in logs_folder:
                logs_folder.replace(linux_divider, self.path_divider)
        else:
            self.path_divider = linux_divider
            if windows_divider in download_folder:
                download_folder.replace(windows_divider, self.path_divider)
            if windows_divider in logs_folder:
                logs_folder.replace(windows_divider, self.path_divider)
        self.logs_folder = logs_folder
        self.download_folder = download_folder

    def search_movie(self, film_name):
        query = SearchTorrentPirateBay(film_name)
        torrents = query.search_film()
        if not torrents:
            self.logger.debug("Couldn't find any torrent!")
        else:
            self.torrents = torrents[:self.MAX_NUM_OF_TORRENTS - 1]

    def download_movie(self, move_torrent: PirateBayFilmTorrent):
        print(f"The following torrent will be downloaded: {move_torrent}")
        self.logger.debug(f"The following torrent will be downloaded: {move_torrent}")
        webbrowser.open(move_torrent.magnet_link)

    def download_subtitles(self):
        subs = Subtitles(api_key=self.opensubtitles_key, log_folder=self.logs_folder)
        year = str(self.torrent_selected.year) if self.torrent_selected.year else None
        for lang in self.language_preferences:
            try:
                subs_file_id = subs.search_subs(lang=lang,
                                                year=year,
                                                resolution=self.torrent_selected.resolution,
                                                quality=self.torrent_selected.quality,
                                                codec=self.torrent_selected.codec,
                                                title=self.torrent_selected.movie_name,
                                                group=self.torrent_selected.group,
                                                excess=self.torrent_selected.excess,
                                                )
                subs.download_subs(lang=lang,
                                   file_name=self.torrent_selected.torrent_name,
                                   film_name_short=self.film_name,
                                   file_id=subs_file_id,
                                   base_folder=self.download_folder)
            except SubtitlesNotFoundException as e:
                print(e)
                self.logger.error(e)
            except DestinationFolderNotFoundException as e:
                print(e)
                self.logger.error(e)
            except Exception as e:
                print(e)
                self.logger.error(e)


@app.route("/")
def home():
    return render_template('home.jinja2', recent_downloads=auto_gui.redis_client.get_recent_downloads)


@app.route('/post/<torrents>')
def torrent(torrents):
    print(torrents)
    return render_template('torrent.jinja2', torrents=torrents)


@app.route('/post/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        film_name = request.form.get('film_name')

        auto_gui.film_name = film_name
        auto_gui.search_movie(film_name)

        if auto_gui.torrents and len(auto_gui.torrents) > 0:
            return redirect(url_for('torrents_results'))
        else:
            msg = f"No torrent was found for: {auto_gui.film_name}..."
            print(msg)
            auto_gui.logger.debug(msg)
            return render_template('error_empty_results.jinja2', film_name=auto_gui.film_name)
    return render_template('search_movie.jinja2')


@app.route('/post/results', methods=['GET', 'POST'])
def torrents_results():
    if request.method == 'POST':
        selected_torrent_index = int(request.form['submit_button']) - 1
        auto_gui.torrent_selected = auto_gui.torrents[selected_torrent_index]
        auto_gui.logger.debug(f"Downloading {auto_gui.torrent_selected.torrent_name}")

        # Check if Torrent selected is in recent downloads.
        is_added = auto_gui.redis_client.add_recent_download(auto_gui.torrent_selected.torrent_name)
        if not is_added:
            msg = f"Torrent was already downloaded: {auto_gui.torrent_selected.torrent_name}..."
            print(msg)
            auto_gui.logger.debug(msg)
            return render_template('torrent_already_exists.jinja2', torrent=auto_gui.torrent_selected.torrent_name)

        auto_gui.download_movie(auto_gui.torrent_selected)

        msg = f"Downloading {auto_gui.torrent_selected}..."
        print(msg)
        auto_gui.logger.debug(msg)
        time.sleep(auto_gui.SLEEP_TIME_AFTER_DL_START)

        auto_gui.download_subtitles()
    return render_template('torrents_results.jinja2', torrents=auto_gui.torrents)


def run(opensubtitles_key, download_folder, language_preferences, logs_folder, system_os=None, port=5000,
        ip_address="0.0.0.0"):

    print(f"Running AutoDownloader App\nListening on http://{ip_address}:{port}")
    global auto_gui
    if not system_os:
        system_os = "linux"

    auto_gui = AutoDownloadGUI(opensubtitles_key=opensubtitles_key,
                               download_folder=download_folder,
                               language_preferences=language_preferences,
                               logs_folder=logs_folder,
                               system_os=system_os)
    app.run(host="0.0.0.0", debug=True, port=port)


if __name__ == '__main__':
    global auto_gui
