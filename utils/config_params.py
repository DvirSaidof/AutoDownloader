import json
import os

class ConfigParams:

    def __init__(self, config_file) -> None:
        
        try:
            with open(config_file, 'r') as f:
                config = json.loads(f.read())
        except FileNotFoundError as error_msg:
            raise FileNotFoundError(error_msg) 

        self._opensubtitles_key = config.get('opensubtitles_credentials').get('api_key')
        self._download_folder = config.get('user_preferences').get('download_folder')
        self._language_preferences = config.get('user_preferences').get('language')
        self._logs_folder = config.get('user_preferences').get('logs_folder')

    @property
    def opensubtitles_key(self):
        return self._opensubtitles_key    
    
    @property
    def download_folder(self):
        return self._download_folder
    
    @property
    def language_preferences(self):
        return self._language_preferences
    
    @property
    def logs_folder(self):
        return self._logs_folder
