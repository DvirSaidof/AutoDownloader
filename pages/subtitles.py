import webbrowser
import requests
import json

#from auto_downloader.constants import SubtitlesConstants
from constants import SubtitlesConstants


class Subtitles:
    """
    The Subtitles class will use movie_name as input and language to download subtitles from
    the internet (opensubtitles api??)
    """
    DL_URL = "https://api.opensubtitles.com/api/v1/download/"
    SEARCH_URL = "https://api.opensubtitles.com/api/v1/subtitles/"

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
            raise SubtitlesNotFoundException(f"Couldn't find subtitles for the title: {title}")
        print(f"Found subtitles! will return {movie_attr.get('files')[0].get('file_name')}")
        return mm_file_id

    def download_subs(self, file_name, file_id, folder):
        data = {
            "file_id": file_id
        }
        response = requests.post(self.DL_URL, headers=self.header, json=data)
        response_json = json.loads(response.content)
        dl_url = response_json.get("link")
        response = requests.get(dl_url)
        print(f"Download {file_name} to {folder}/{file_name}.srt")
        with open(folder + f"/{file_name}.srt", 'wb') as f:
            f.write(response.content)


class SubtitlesNotFoundException(FileNotFoundError):
    """Custom Exception"""

