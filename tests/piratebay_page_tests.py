import unittest
from datetime import timedelta, datetime
from pages.piratebay_page import SearchTorrentPirateBay
from constants import PirateBayWebConstants


class PirateBayTorrentTests(unittest.TestCase):

    def setUp(self) -> None:
        self.film_name = "The Lord of the rings"

    def test_parse_search_query_correct(self):
        search_query = SearchTorrentPirateBay(self.film_name)
        self.assertEqual(search_query._parse_search_query,
                         self.film_name.strip().replace(" ", "%20") + PirateBayWebConstants.VIDEO_ON_POSTFIX)

    def test_parse_search_value_error(self):
        film_names = [None, 10, ""]
        for i, film_name in enumerate(film_names):
            with self.subTest(test_number=f"Test # {i}"):
                with self.assertRaises(ValueError):
                    SearchTorrentPirateBay(film_name)

    def test_search_film_exist(self):
        search_query = SearchTorrentPirateBay(self.film_name)
        film_torrents = search_query.search_film()
        self.assertGreater(len(film_torrents), 0)

    def test_search_film_doesnt_exist(self):
        search_query = SearchTorrentPirateBay("a-movie-which-does-not-exists")
        film_torrents = search_query.search_film()
        self.assertEqual(len(film_torrents), 0)