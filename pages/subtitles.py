import webbrowser
import requests
import json
import os
import pathlib
from constants import SubtitlesConstants
from pathlib import Path

class Subtitles:
    """
    The Subtitles class will use movie_name as input and language to download subtitles from
    the internet (opensubtitles api??)
    """
    DL_URL = "https://api.opensubtitles.com/api/v1/download/"
    SEARCH_URL = "https://api.opensubtitles.com/api/v1/subtitles/"
    FILE_TYPES = ('.m1v', '.mpeg', '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4')


    def __init__(self, api_key):
        self.header = {
            'Content-type': 'application/json',
            'Api-Key': api_key
        }
        self.most_matches = dict()

    def _parse_movie_name(self, file_name):
        pass

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
        print(f"Searching for {title} Subtitles")
        mm_file_id = None
        search_query = f"{self.SEARCH_URL}?languages={SubtitlesConstants.LANGUAGES_CODES.get(lang)}&query={title}"
        if year:
            search_query = search_query + f"&year={year}"

        print(search_query)
        try:
            response = requests.get(search_query, headers=self.header)
            json_content = json.loads(response.content)
        except requests.exceptions.MissingSchema as e:
            raise requests.exceptions.MissingSchema(e)
        except requests.exceptions.InvalidSchema as e:
            raise requests.exceptions.InvalidSchema(e)
        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError(e)

        movie_attrs = [resolution, quality, codec, group]
        print(f"Check all attrs: {movie_attrs}")
        most_matches = 0
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
        print(f"Found subtitles! will return {movie_attr.get('files')[0].get('file_name')}")
        return mm_file_id

    def get_dl_file_folder_path(self, base_folder, film_name_short):
        print(f"Trying to find {film_name_short}  Folder inside {base_folder}")

        file_path = pathlib.Path(base_folder)
        film_name_short_first_vers = film_name_short.replace(" ", ".")

        for td in file_path.glob("*"):
            print(td.name)
            if td.is_dir() and \
                    (film_name_short_first_vers.lower() in td.name.lower() or film_name_short.lower() in td.name.lower()):
                return base_folder + "/" + td.name
        else:
            raise MovieFolderNotFound(f"The movie's: {film_name_short} folder wasn't found in: {base_folder}")

    def get_dl_file_name(self, movie_folder: str, film_name_short: str):
        print(f"Trying to find {film_name_short} movie inside {movie_folder}")

        file_path = pathlib.Path(movie_folder)
        film_name_short_first_vers = film_name_short.replace(" ", ".")

        for td in file_path.glob("*"):
            if td.is_file() and td.name.endswith(tuple(self.FILE_TYPES)) \
                    and (film_name_short_first_vers.lower() in td.name.lower() or film_name_short.lower() in td.name.lower()):
                        return Path(f'{movie_folder}/{td.name}').stem # This will return the movie name found without it's video extension
        else:
            return False

    def create_new_folder(self, parent_dir, new_folder):
        print(f"Creating new directoy {parent_dir}/{new_folder}")
        try:
            path = os.path.join(parent_dir, new_folder)
            os.mkdir(path)
        except OSError as error:
            print(error)
            raise OSError(f"Couldn't create new directory {new_folder}. in {parent_dir}")

    def move_movie_to_folder(self, movie_to_move, current_folder, dest_folder):
        print(f"Changing {movie_to_move} directory to {dest_folder}/{movie_to_move}")
        os.chdir(current_folder)
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        try:
            os.rename(f"{movie_to_move}.mp4", f"{dest_folder}/{movie_to_move}")
        except OSError as error:
            print(error)
            raise OSError(f"Failed to move {current_folder}/{movie_to_move} to {dest_folder}/{movie_to_move}")

    def creating_subs_file(self, content, movie_name, movie_folder):
        print(f"Download {movie_name}.srt to {movie_folder}/{movie_name}.srt")
        with open(f"{movie_folder}/{movie_name}.srt", 'wb') as f:
            f.write(content)

    def download_subs(self, file_name: str, film_name_short: str, file_id, base_folder: str):
        print(f"Downloading {file_name} Subtitles")

        data = {
            "file_id": file_id
        }

        response = requests.post(self.DL_URL, headers=self.header, json=data)
        response_json = json.loads(response.content)
        dl_url = response_json.get("link")
        response = requests.get(dl_url)

        try:
            movie_folder = self.get_dl_file_folder_path(base_folder, film_name_short)
            print(f"Movie folder is: {movie_folder}")
        except MovieFolderNotFound as e:
            print(e)
            movie_folder = base_folder
            # movie_name = self.get_dl_file_name(base_folder, film_name_short)
            # if not movie_name:
            #     raise MovieFolderNotFound("The movie folder wasn't found. Probably the download didn't start")
            # else:
            #     print(f"Movie file name is: {movie_name}")
            #     new_folder = movie_name
            #     self.create_new_folder(base_folder, new_folder)
            #     self.move_movie_to_folder(movie_name, base_folder, new_folder)
            #     self.creating_subs_file(response.content, movie_name, f'{base_folder}/{new_folder}')
            #     return
        try:
            movie_name = self.get_dl_file_name(movie_folder, film_name_short)
            print(f"Movie file name is: {movie_name}")
            self.creating_subs_file(response.content, movie_name, movie_folder)
        except FileNotFoundError as e:
            raise DestinationFolderNotFoundException(f"Movie destination folder for {file_name} was not found.\n {e}")

class SubtitlesNotFoundException(FileNotFoundError):
    """Custom Exception"""

class DestinationFolderNotFoundException(FileNotFoundError):
    """Custom Exception"""

class MovieFolderNotFound(FileNotFoundError):
    """Custom Exception"""

