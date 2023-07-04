import unittest
import os
from utils.config_params import ConfigParams
from subtitles_api.subtitles import Subtitles, SubtitlesNotFoundException, DestinationFolderNotFoundException
from subtitles_api.tests.test_constants import SubtitlesTestConstants

class SubtitlesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if not cls.perform_initial_setup():
            cls.skipTest(cls, "Initial setup failed. Aborting remaining tests in .")
        
    @classmethod
    def perform_initial_setup(cls):
        
        module_path = os.path.abspath(os.path.dirname(__file__))
        cls.config_json_path = os.path.join(module_path, SubtitlesTestConstants.CONFIG_JSON_PATH)
        
        if not cls.config_json_path:
            print("config_json_path is empty!")
            return False
        
        cls.config_obj = ConfigParams(cls.config_json_path)

        if not cls.config_obj.opensubtitles_key:
            print("opensubtitles_key is empty!")
            return False

        try:
            # TODO: We will need to validate the opensubtitles key somehow
            cls.subs_obj = Subtitles(
                cls.config_obj.opensubtitles_key,        
                log_folder=cls.config_obj.logs_folder
            )
        except ValueError as error:
            print("Subtitles object returned error!")
            return False

        return True

    def test_api_wrong_key_error(self):
        wrong_api_keys = [None, 10, ""]
        for i, wrong_api_key in enumerate(wrong_api_keys):
            with self.subTest(test_number=f"Test # {i}"):
                with self.assertRaises(ValueError):
                    Subtitles(wrong_api_key, log_folder=self.config_obj.logs_folder)

    def test_download_subs_right_dir(self):

        file_id = self.subs_obj.search_subs(
            lang=SubtitlesTestConstants.LANG, 
            title=SubtitlesTestConstants.TITLE, 
            year=SubtitlesTestConstants.YEAR, 
            resolution=SubtitlesTestConstants.RESOLUTION, 
            quality=SubtitlesTestConstants.QUALITY, 
            codec=SubtitlesTestConstants.CODEC, 
            group=SubtitlesTestConstants.GROUP,
            excess=SubtitlesTestConstants.EXCESS
        )
        
        folder_path = self.config_obj.download_folder
        file_name = f"{SubtitlesTestConstants.MOVIE_FILE_NAME}-{SubtitlesTestConstants.LANG}.srt"
        file_path = os.path.join(folder_path, file_name)

        self.subs_obj.download_subs(
            SubtitlesTestConstants.LANG, 
            SubtitlesTestConstants.MOVIE_FILE_NAME, 
            SubtitlesTestConstants.MOVIE_FILE_NAME, 
            file_id, 
            folder_path
        )

        self.assertTrue(os.path.exists(file_path), f"File '{file_name}' does not exist in folder '{folder_path}'.")


    def test_search_subs_best_fit(self):    
        pass
