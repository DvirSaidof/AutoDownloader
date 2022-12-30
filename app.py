import logging
import webbrowser
from google.auth.exceptions import RefreshError
from OpenSSL.crypto import Error
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
# from typing import List, Dict
import time
import json

from pages.subtitles import Subtitles, SubtitlesNotFoundException, DestinationFolderNotFoundException
from utils.google_connect import GoogleConnection
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
    GOOGLE_SHEET_UI_SLEEP = 60

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
        self._get_film_to_dl_from_google_sheet()
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

    def write_result_to_google_sheet(self):
        try:
            with GoogleConnection(self.google_credentials) as client:
                sheet = client.open("AutoDownloadApp")
                worksheet = sheet.get_worksheet(1)
        except WorksheetNotFound:
            print("Result sheet not found. creating one..")
            self.logger.debug("Creating new sheet named OutputSheet")
            worksheet = sheet.add_worksheet(title="OutputSheet", rows=100, cols=20)
            for cell, title in AutoDownloadApp.TITLE_CELLS.items():
                worksheet.update(cell, title)
            worksheet.format('A1:F1', {'textFormat': {'bold': True}})
            for i in range(2, 12):
                worksheet.update(f'A{i}', i - 1)
        except FileNotFoundError as e:
            print(f"Credentials file config/google_credentials.json is missing. {e}")
            raise
        except RefreshError as e:
            print(f"client_email value is wrong. {e}")
            raise
        except Error as e:
            print(f"private_key value is wrong. {e}")
            raise
        except SpreadsheetNotFound as e:
            print(f"Can't find spreadsheet. Make sure the spreadsheet was created. {e}")
            raise
        except Exception as e:
            print(e)
            raise
        self._update_worksheet(worksheet)

    def print_torrents(self):
        for torrent in self.torrents_options.values():
            print(torrent)

    def change_list_of_torrents(self):
        for torrent in self.torrents:
            self.torrents_list.append(
                [torrent.type, torrent.torrent_name,
                 torrent.size, torrent.seeds, torrent.leechers])

    def _update_worksheet(self, worksheet):
        self.change_list_of_torrents()
        num_of_results = len(self.torrents_list) + 1
        worksheet.update(f'B2:F{num_of_results}', self.torrents_list)

    def _get_film_to_dl_from_google_sheet(self):
        try:
            with GoogleConnection(self.google_credentials) as client:
                sheet = client.open("AutoDownloadApp").sheet1
                self.film_name = sheet.cell(2, 1).value
        except FileNotFoundError as e:
            print(f"Credentials file config/google_credentials.json is missing. {e}")
            raise
        except RefreshError as e:
            print(f"client_email value is wrong. {e}")
            raise
        except Error as e:
            print(f"private_key value is wrong. {e}")
            raise
        except SpreadsheetNotFound as e:
            print(f"Can't find spreadsheet. Make sure the spreadsheet was created. {e}")
            raise
        except Exception as e:
            print(e)
            raise

    # create wrapper!!
    # def google_connection_wrapper(self, func):
    #     try:
    #         with GoogleConnection(self.google_credentials) as client:
    #             func()
    #     except FileNotFoundError as e:
    #         print(f"Credentials file config/google_credentials.json is missing. {e}")
    #         raise
    #     except RefreshError as e:
    #         print(f"client_email value is wrong. {e}")
    #         raise
    #     except Error as e:
    #         print(f"private_key value is wrong. {e}")
    #         raise
    #     except SpreadsheetNotFound as e:
    #         print(f"Can't find spreadsheet. Make sure the spreadsheet was created. {e}")
    #         raise
    #     except Exception as e:
    #         print(e)
    #         raise
    def wait_for_user_selection(self):
        try:
            with GoogleConnection(self.google_credentials) as client:
                user_selection = None
                current_time = time.time()
                while not user_selection or user_selection == "":
                    msg = f"Waiting for user input.. Seconds left to select " \
                          f"{UserInputTimeOutException.TIMEOUT - (time.time() - current_time)}"
                    print(msg)
                    self.logger.debug(msg)

                    time.sleep(self.GOOGLE_SHEET_UI_SLEEP)
                    sheet = client.open("AutoDownloadApp")
                    data = sheet.get_worksheet(0)
                    user_selection = data.cell(2, 3).value
                    if time.time() - current_time > UserInputTimeOutException.TIMEOUT:
                        raise UserInputTimeOutException(f"Timeout! {UserInputTimeOutException.TIMEOUT} "
                                                        f"seconds has passed.")
                return int(user_selection) - 1
        except FileNotFoundError as e:
            print(f"Credentials file config/google_credentials.json is missing. {e}")
            self.clear_sheets()
            raise
        except RefreshError as e:
            print(f"client_email value is wrong. {e}")
            self.clear_sheets()
            raise
        except Error as e:
            print(f"private_key value is wrong. {e}")
            self.clear_sheets()
            raise
        except SpreadsheetNotFound as e:
            print(f"Can't find spreadsheet. Make sure the spreadsheet was created. {e}")
            self.clear_sheets()
            raise
        except IndexError as e:
            print(e)
            self.clear_sheets()
            raise
        except AttributeError as e:
            print(e)
            self.clear_sheets()
            raise
        except Exception as e:
            print(e)
            self.clear_sheets()
            raise

    def google_sheet_interactive(self, film_name):
        self.film_name = film_name
        self.logger.debug(f"Searching for movie: {self.film_name}")
        self.search_movie()
        if self.torrents and len(self.torrents) > 0:
            self.logger.debug("Writing the result to a google sheet")
            self.write_result_to_google_sheet()
            self.logger.debug("Waiting for user selection")
            user_selection = self.wait_for_user_selection()
            self.torrent_selected = self.torrents[user_selection]
            self.logger.debug(f"User selected: {user_selection}")
            self.download_movie(self.torrent_selected)
            msg = f"Downloading {self.torrent_selected}..."
            print(msg)
            self.logger.debug(msg)
            time.sleep(self.SLEEP_TIME_AFTER_DL_START)
            subs = Subtitles(self.opensubtitles_key)
            year = str(self.torrent_selected.year) if self.torrent_selected.year else None
            # {'year': 1976, 'resolution': '720p', 'quality': 'BrRip', 'codec': 'x264', 'title': 'Rocky', 'group': 'YIFY', 'excess': '750MB'}
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
                                       film_name_short=film_name,
                                       file_id=subs_file_id,
                                       base_folder=self.folder)
                except SubtitlesNotFoundException as e:
                    print(e)
                    self.logger.error(e)
                except DestinationFolderNotFoundException as e:
                    print(e)
                    self.logger.error(e)
                except Exception as e:
                    print(e)
                    self.logger.error(e)
        else:
            msg = "No movie was found"
            print(msg)
            self.logger.debug(msg)

    def download_movie(self, torrent: PirateBayFilmTorrent):
        print(f"The following torrent will be downloaded: {torrent}")
        self.logger.debug(f"The following torrent will be downloaded: {torrent}")
        webbrowser.open(torrent.magnet_link)

    def clear_sheets(self):
        with GoogleConnection(self.google_credentials) as client:
            sheet = client.open("AutoDownloadApp")
            input_sheet = sheet.get_worksheet(0)
            output_sheet = sheet.get_worksheet(1)
            input_sheet.batch_clear(["A2:C2"])
            output_sheet.batch_clear(["B2:F11"])
        self.torrents_list = []


def run(credentials):
    while True:
        msg = "Program is running and searching for a search input"
        logging.info(msg)
        print(msg)

        time.sleep(AutoDownloadApp.GOOGLE_SHEET_UI_SLEEP)

        ad_client = AutoDownloadApp(credentials)
        with GoogleConnection(ad_client.google_credentials) as client:
            sheet = client.open("AutoDownloadApp")
            input_sheet = sheet.get_worksheet(0)
            film_name = input_sheet.cell(2, 1).value
            if film_name:
                print(f"Will search and download {film_name}")
                try:
                    ad_client.google_sheet_interactive(film_name)
                except Exception as e:
                    msg = "There was an Error during "
                    logging.info(msg)
                    print(msg)
                    time.sleep(AutoDownloadApp.GOOGLE_SHEET_UI_SLEEP)
                finally:
                    ad_client.clear_sheets()

class UserInputTimeOutException(TimeoutError):
    """
    will be raised when user didn't respond to application for a TIMEOUT interval of time
    """
    TIMEOUT = 300
    pass

if __name__ == "__main__":
    run("config/config.json")
