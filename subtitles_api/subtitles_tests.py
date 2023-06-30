import unittest
from subtitles_api.subtitles import Subtitles, SubtitlesNotFoundException, DestinationFolderNotFoundException


class SubtitlesTests(unittest.TestCase):

    def test_api_wrong_key_error(self):
        wrong_api_keys = [None, 10, ""]
        for i, wrong_api_key in enumerate(wrong_api_keys):
            with self.subTest(test_number=f"Test # {i}"):
                with self.assertRaises(ValueError):
                    Subtitles(wrong_api_key, log_folder="logs")

    def test_search_subs_best_fit(self):
        # TODO
        pass

    def download_subs_right_dir(self):
        # TODO
        pass

    def download_subs_right_subs(self):
        # TODO
        pass
