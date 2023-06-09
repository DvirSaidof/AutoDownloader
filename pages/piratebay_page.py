from bs4 import BeautifulSoup
from typing import List
import requests

from constants import PirateBayWebConstants
from locators.pb_page_locators import PrimaryPBTorrentPageLocators
from parsers.piratebay_torrent import PirateBayFilmTorrent


class SearchTorrentPirateBay:
    """
    SearchTorrentPirateBay Class allows to make search queries on PirateBay, with
    www1.thepiratebay3.to domain using the search_film method.
    """
    def __init__(self, film_name):
        if not film_name or not isinstance(film_name, str):
            raise ValueError("The film name is either None or empty or not of str type")
        self.film_name = film_name
        self.soup = None
        self.torrents = []

    @property
    def _parse_search_query(self):
        return self.film_name.strip().replace(" ", "%20") + PirateBayWebConstants.VIDEO_ON_POSTFIX

    @property
    def _get_films_table(self):
        response = requests.get(
            PirateBayWebConstants.PB_DOMAIN_PRIMARY +
            PirateBayWebConstants.SEARCH_BY_SEEDS_PREFIX_PRIMARY +
            self._parse_search_query)
        response.raise_for_status()
        return response.content

    def search_film(self) -> List[PirateBayFilmTorrent]:
        self.soup = BeautifulSoup(self._get_films_table, "html.parser")
        locator = PrimaryPBTorrentPageLocators.TORRENT_LOCATOR
        torrents_tags = self.soup.select(locator)
        self.torrents = [PirateBayFilmTorrent(torrent_tag) for torrent_tag in torrents_tags]
        return self.torrents

    def print_torrents(self) -> None:
        for film_torrent in self.torrents:
            print(film_torrent)


class InvalidTagForTorrentError(Exception):
    pass
