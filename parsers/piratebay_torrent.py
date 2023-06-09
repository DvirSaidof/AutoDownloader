import requests
from bs4 import BeautifulSoup
import PTN

#from auto_downloader.locators.pb_torrent_locators import PrimaryPBFilmTorrentLocators
from locators.pb_torrent_locators import PrimaryPBFilmTorrentLocators
#from constants import PirateBayWebConstants
from constants import PirateBayWebConstants


class PirateBayFilmTorrent:

    def __init__(self, parent):
        self.parent = parent
        #{'year': 1976, 'resolution': '720p', 'quality': 'BrRip', 'codec': 'x264', 'title': 'Rocky', 'group': 'YIFY', 'excess': '750MB'}
        if self.torrent_name:
            movie_info = PTN.parse(self.torrent_name)
            self.year = movie_info.get("year")
            self.resolution = movie_info.get("resolution")
            self.quality = movie_info.get("quality")
            self.codec = movie_info.get("codec")
            self.movie_name = movie_info.get("title")
            self.group = movie_info.get("group")
            self.excess = movie_info.get("excess")

    def __repr__(self):
        return f"<({self.type}), {self.torrent_name}, Torrent size: {self.size}, " \
               f"Seeders: {self.seeds}>"

    @property
    def type(self):
        locator = PrimaryPBFilmTorrentLocators.TORRENT_TYPE_LOCATOR
        try:
            return self.parent.select_one(locator).string
        except AttributeError:
            return

    @property
    def torrent_name(self):
        locator = PrimaryPBFilmTorrentLocators.TORRENT_NAME_LOCATOR
        try:
            return self.parent.select_one(locator).string
        except AttributeError:
            return

    @property
    def size(self):
        try:
            return self._size_and_seeds_tags("size")
        except AttributeError:
            return

    @property
    def leechers(self):
        return 0

    @property
    def seeds(self):
        try:
            return self._size_and_seeds_tags("seeds")
        except AttributeError:
            return

    @property
    def magnet_link_page(self):
        locator = PrimaryPBFilmTorrentLocators.TORRENT_NAME_LOCATOR
        try:
            return PirateBayWebConstants.PB_DOMAIN_PRIMARY + self.parent.select_one(locator).attrs.get('href')
        except AttributeError:
            return

    @property
    def magnet_link(self):
        response = requests.get(self.magnet_link_page)
        response.raise_for_status()

        magnet_link_page_soup = BeautifulSoup(response.content, "html.parser")
        locator = PrimaryPBFilmTorrentLocators.TORRENT_MAGNET_URL
        try:
            return magnet_link_page_soup.select_one(locator).attrs.get('href')
        except AttributeError:
            return

    def _size_and_seeds_tags(self, tag):
        locator = PrimaryPBFilmTorrentLocators.TORRENT_SIZE_SEEDS_LOCATOR
        size, seeds, *xargs = self.parent.select(locator)
        if tag == "size":
            return size.string
        elif tag == "seeds":
            return seeds.string
