import unittest
from subtitles_api.subtitles import Subtitles, SubtitlesNotFoundException, DestinationFolderNotFoundException


class SubtitlesTests(unittest.TestCase):

    def test_api_key_correct(self):
        wrong_api_keys = [None, 10, ""]
        for i, wrong_api_key in enumerate(wrong_api_keys):
            with self.subTest(test_number=f"Test # {i}"):
                with self.assertRaises(ValueError):
                    Subtitles(wrong_api_key)

    def test_get_dl_file_folder_path(self):
        # TODO
        pass
