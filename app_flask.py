import logging
import webbrowser
import gui.gui as gui
from typing import List, Dict
import time
import json

from pages.subtitles import Subtitles, SubtitlesNotFoundException, DestinationFolderNotFoundException
from pages.pb_torrents_page import SearchTorrentPirateBay
from parsers.pb_torrent_parser import PirateBayFilmTorrent

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S', level=logging.DEBUG, filename='auto_download_app.log')

logging.FileHandler('auto_download_app.log', 'w', 'utf-8')
logging.getLogger("app")


class AutoDownloadApp:
    """
    The AutoDownloadApp interacts with the user/google doc files and receive a file_name to download.
    It will then perform a search query on PirateBay using SearchTorrentPirateBay Class, and download the best result
    (E.G torrent with most seeders).
    Download the torrent using webbroswer module to open UTorrent.
    Download subtitles with Subtitles Class which gets language preferences
    Place all files in a shared folder on a local or remote machine.
    """

    TITLE_CELLS = {'A1': 'Select', 'B1': 'Type', 'C1': 'Name', 'D1': 'Size', 'E1': 'Seeders', 'F1': 'Leechers'}
    MAX_NUM_OF_TORRENTS = 15
    SLEEP_TIME_AFTER_DL_START = 30
    GOOGLE_SHEET_UI_SLEEP = 20

    def __init__(self, credentials):
        with open(credentials) as f:
            self.credentials = json.loads(f.read())
        with open("config/google_creds.json", "w") as outfile:
            json.dump(self.credentials.get('google_credentials'), outfile)
        self.torrents_list = []
        self.film_name = None
        self.torrents_options = dict()
        self.torrents = []
        self.torrent_selected = None
        self.google_credentials = "config/google_creds.json"
        self.opensubtitles_key = self.credentials.get('opensubtitles_credentials').get('api_key')
        self.folder = self.credentials.get('user_preferences').get('folder')
        self.language_preferences = self.credentials.get('user_preferences').get('language')
        #self._get_film_to_dl_from_google_sheet()
        self.logger = logging.getLogger("app.AutoDownloadApp")

    def search_movie(self):
        query = SearchTorrentPirateBay()
        self.torrents = query.search_film(self.film_name)
        if not self.torrents:
            print("Couldn't find any torrent!")
        else:
            self.torrents = self.torrents[:AutoDownloadApp.MAX_NUM_OF_TORRENTS - 1]

    def download_subtitles(self):
        pass

    def _create_menu_dict(self):
        for i in range(1, AutoDownloadApp.MAX_NUM_OF_TORRENTS):
            self.torrents_options[i] = self.torrents[i - 1]

    def menu(self):
        self._create_menu_dict()
        user_input = 0
        while int(user_input) not in self.torrents_options.keys() and user_input != 'q':
            print("Please select a torrent to Download")
            for key, val in self.torrents_options.items():
                print(key, '--', self.torrents_options.get(key))
            user_input = input("Please insert a number: ")
        else:
            print("Quiting..")


    def change_list_of_torrents(self):
        for torrent in self.torrents:
            self.torrents_list.append(
                [torrent.type, torrent.torrent_name,
                 torrent.size, torrent.seeds, torrent.leechers])



    def download_movie(self, torrent: PirateBayFilmTorrent):
        print(f"The following torrent will be downloaded: {torrent}")
        self.logger.debug(f"The following torrent will be downloaded: {torrent}")
        webbrowser.open(torrent.magnet_link)


def run(credentials):
    print("Running gui")
    gui.run() ######################################################################################
    while True:
        msg = "Program is running and searching for a search input"
        logging.info(msg)
        print(msg)
        time.sleep(AutoDownloadApp.GOOGLE_SHEET_UI_SLEEP)
        #ad_client = AutoDownloadApp(credentials)
        film_name = gui.get_movie_name
        film_year = gui.get_movie_year
        print(film_name)
        #print(f"blaaaaa: {film_name} and year: {film_year}")
        # if film_name:
        #     print(f"Will search and download {film_name}")
        #     try:
        #         ad_client.google_sheet_interactive(film_name)
        #     except Exception as e:
        #         msg = "There was an Error during "
        #         logging.info(msg)
        #         print(msg)
        #         time.sleep(AutoDownloadApp.GOOGLE_SHEET_UI_SLEEP)
        #     finally:
        #         ad_client.clear_sheets()


class UserInputTimeOutException(TimeoutError):
    """
    will be raised when user didn't respond to application for a TIMEOUT interval of time
    """
    TIMEOUT = 300
    pass


if __name__ == "__main__":
    run("config/config.json")
