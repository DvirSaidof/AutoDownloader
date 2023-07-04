import logging
import requests
import json
import os
import pathlib
import sys
from subtitles_api.constants import SubtitlesConstants
from pathlib import Path


class Subtitles:
    """
    The Subtitles class will use movie_name as input and language to download subtitles from
    the internet (opensubtitles api??)
    """

    # TODO: We will need to validate the opensubtitles key somehow
    def __init__(self, api_key, logger=None, log_folder='/var/logs'):

        self.path_divider = "/"
        if sys.platform.startswith("win"):
            self.path_divider = "\\"

        if logger and isinstance(logger, logging.Logger):
            self.logger = logger
        else:
            logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                datefmt='%d-%m-%Y:%H:%M:%S', level=logging.DEBUG,
                                filename=f'{log_folder}{self.path_divider}subtitles.log')
            logging.FileHandler(f'{log_folder}{self.path_divider}subtitles.log', 'w', 'utf-8')
            self.logger = logging.getLogger("subtitles")

        if not api_key or not isinstance(api_key, str):
            msg = "Api key wasn't configured or is not of type str"
            self._print_log(msg)
            raise ValueError(msg)

        self.header = {
            'Content-type': 'application/json',
            'Api-Key': api_key
        }
        self.most_matches = dict()


    def _print_log(self, msg):
        print(msg)
        self.logger.debug(msg)

    def _get_dl_file_folder_path(self, base_folder, film_name_short):
        self._print_log(f"Trying to find {film_name_short}  Folder inside {base_folder}")

        file_path = pathlib.Path(base_folder)
        film_name_short_first_vers = film_name_short.replace(" ", ".")

        for td in file_path.glob("*"):
            print(td.name)
            if td.is_dir() and \
                    (film_name_short_first_vers.lower() in td.name.lower() or 
                     film_name_short.lower() in td.name.lower()):
                return base_folder + self.path_divider + td.name
        else:
            raise MovieFolderNotFound(f"The movie's: {film_name_short} folder wasn't found in: {base_folder}")

    def _creating_subs_file(self, content, movie_name, movie_folder, lang):
        self._print_log(f"Download {movie_name}.srt to {movie_folder}{self.path_divider}{movie_name}.srt")
        with open(f"{movie_folder}{self.path_divider}{movie_name}-{lang}.srt", 'wb') as f:
            f.write(content)

    def _get_dl_file_name(self, movie_folder: str, film_name_short: str):
        self._print_log(f"Trying to find {film_name_short} movie inside {movie_folder}")

        file_path = pathlib.Path(movie_folder)
        film_name_short_first_vers = film_name_short.replace(" ", ".")

        # This will return the movie name found without it's video extension
        for td in file_path.glob("*"):
            if td.is_file() and td.name.endswith(tuple(SubtitlesConstants.FILE_TYPES)) and\
                    (film_name_short_first_vers.lower() in td.name.lower() or
                     film_name_short.lower() in td.name.lower()):
                return Path(f'{movie_folder}{self.path_divider}{td.name}').stem
        else:
            return False

    def _create_new_folder(self, parent_dir, new_folder):
        self._print_log(f"Creating new directoy {parent_dir}{self.path_divider}{new_folder}")
        try:
            path = os.path.join(parent_dir, new_folder)
            os.mkdir(path)
        except OSError as error:
            print(error)
            raise OSError(f"Couldn't create new directory {new_folder}. in {parent_dir}")

    def _move_movie_to_folder(self, movie_to_move, current_folder, dest_folder):
        self._print_log(f"Changing {movie_to_move} directory to {dest_folder}{self.path_divider}{movie_to_move}")
        os.chdir(current_folder)
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        try:
            os.rename(f"{movie_to_move}.mp4", f"{dest_folder}{self.path_divider}{movie_to_move}")
        except OSError as error:
            print(error)
            raise OSError(f"Failed to move {current_folder}{self.path_divider}{movie_to_move} to {dest_folder}{self.path_divider}{movie_to_move}")

    def download_subs(self, lang: str, file_name: str, film_name_short: str, file_id, base_folder: str):
        self._print_log(f"Downloading {file_name} Subtitles")

        data = {
            "file_id": file_id
        }

        response = requests.post(SubtitlesConstants.DL_URL, headers=self.header, json=data)
        response_json = json.loads(response.content)
        dl_url = response_json.get("link")
        response = requests.get(dl_url)

        try:
            movie_folder = self._get_dl_file_folder_path(base_folder, film_name_short)
            self._print_log(f"Movie folder is: {movie_folder}")
        except MovieFolderNotFound as e:
            self._print_log(e)
            movie_folder = base_folder
        try:
            movie_name = self._get_dl_file_name(movie_folder, film_name_short)
            if not movie_name:
                movie_name = file_name.title()
            self._print_log(f"Movie file name is: {movie_name}")
            self._creating_subs_file(response.content, movie_name, movie_folder, lang)
        except FileNotFoundError as e:
            raise DestinationFolderNotFoundException(f"Movie destination folder for {file_name} was not found.\n {e}")

    def search_subs(self, lang, title: str, year: str, resolution: str, quality: str, codec: str, group: str, excess: str) -> str:
        """
        Example:
        :param lang: he,en,ru,it,es
        :param title: Rocky
        :param year: 1976
        :param resolution: 720p
        :param quality: BrRip
        :param codec: x264
        :param group: YIFY
        :param excess: 750MB
        :return: file_id
        """
        self._print_log(f"Searching for {title} Subtitles")
        mm_file_id = None
        search_query = f"{SubtitlesConstants.SEARCH_URL}?languages=" \
                       f"{SubtitlesConstants.LANGUAGES_CODES.get(lang)}&query={title}"
        if year:
            search_query = search_query + f"&year={year}"

        self._print_log(search_query)
        try:
            response = requests.get(search_query, headers=self.header)
            print(f"response zaken = {response}")
            json_content = json.loads(response.content)
        except requests.exceptions.MissingSchema as e:
            raise requests.exceptions.MissingSchema(e)
        except requests.exceptions.InvalidSchema as e:
            raise requests.exceptions.InvalidSchema(e)
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError(e)

        movie_attrs = [resolution, quality, codec, group]
        self._print_log(f"Check all attrs: {movie_attrs}")
        most_matches = 0

        movie_attr = ""
        
        for movie_subs in json_content.get('data'):
            movie_attr = movie_subs.get('attributes')
            file_id = movie_attr.get('files')[0].get('file_id')
            release = movie_attr.get("release")
            self.most_matches[file_id] = 0
            num_of_matches = 0
            if resolution and resolution in release:
                num_of_matches += 1
            if quality and quality in release:
                num_of_matches += 1
            if codec and codec in release:
                num_of_matches += 1
            if group and group in release:
                num_of_matches += 1
            if num_of_matches > most_matches:
                most_matches = num_of_matches
                mm_file_id = file_id

        if not mm_file_id:
            raise SubtitlesNotFoundException(f"Couldn't find subtitles for the movie: {title}")
        self._print_log(f"Found subtitles! will return {movie_attr.get('files')[0].get('file_name')}")
        return mm_file_id


class SubtitlesNotFoundException(FileNotFoundError):
    """Custom Exception"""


class DestinationFolderNotFoundException(FileNotFoundError):
    """Custom Exception"""


class MovieFolderNotFound(FileNotFoundError):
    """Custom Exception"""
