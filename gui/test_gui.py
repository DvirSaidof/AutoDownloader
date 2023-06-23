import unittest
import gui.gui as gui
import json
import sys

from gui.gui import AutoDownloadGUI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class AutoDownloadGUITests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_search_movie(self):
        #self.driver.get("https://0.0.0.0:5000")
        pass

    def test_download_movie(self):
        # TODO
        pass

    def test_download_subs(self):
        pass
