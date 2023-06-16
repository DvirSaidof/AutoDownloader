import unittest
from piratebay_api.tests.piratebay_page_tests import PirateBayTorrentTests
from subtitles_api.subtitles_tests import SubtitlesTests
from gui.gui import AutoDownloadGUI


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


run_tests(PirateBayTorrentTests)
run_tests(SubtitlesTests)
run_tests(AutoDownloadGUI)
