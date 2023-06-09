import unittest
from piratebay_page_tests import PirateBayTorrentTests


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


run_tests(PirateBayTorrentTests)