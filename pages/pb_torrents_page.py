from bs4 import BeautifulSoup
from typing import List
import requests

#from auto_downloader.constants import PirateBayWebConstants
from constants import PirateBayWebConstants
#from auto_downloader.locators.pb_page_locators import PrimaryPBTorrentPageLocators
from locators.pb_page_locators import PrimaryPBTorrentPageLocators
#from auto_downloader.parsers.pb_torrent_parser import PirateBayFilmTorrent
from parsers.pb_torrent_parser import PirateBayFilmTorrent


class SearchTorrentPirateBay:
    """
    SearchTorrentPirateBay Class allows to make search queries on PirateBay, with
    www1.thepiratebay3.to domain using the search_film method.
    """
    def __init__(self):
        self.film_name = None
        self.film_search_query = None
        self.soup = None

    @property
    def _parse_search_query(self):
        try:
            search_query = self.film_name.strip().replace(" ", "%20") + PirateBayWebConstants.VIDEO_ON_POSTFIX
            return search_query
        except AttributeError:
            print("Failed. couldn't create the search query. won't download anything")

    @property
    def _get_films_table(self):
        response = requests.get(
            PirateBayWebConstants.PB_DOMAIN_PRIMARY +
            PirateBayWebConstants.SEARCH_BY_SEEDS_PREFIX_PRIMARY +
            self.film_search_query)
        response.raise_for_status()
        return response.content

    def search_film(self, film_name: str) -> List[PirateBayFilmTorrent]:
        self.film_name = film_name
        self.film_search_query = self._parse_search_query
        if self._parse_search_query:
            self.soup = BeautifulSoup(self._get_films_table, "html.parser")
            locator = PrimaryPBTorrentPageLocators.TORRENT_LOCATOR
            torrents_tag = self.soup.select(locator)
            return [PirateBayFilmTorrent(torrent_tag) for torrent_tag in torrents_tag]

    @classmethod
    def print_torrents(cls, film_torrents: List[PirateBayFilmTorrent]) -> None:
        for film_torrent in film_torrents:
            print(film_torrent)


class InvalidTagForTorrentError(Exception):
    pass
