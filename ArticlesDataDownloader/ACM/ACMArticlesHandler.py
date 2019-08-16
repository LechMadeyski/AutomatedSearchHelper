
import selenium
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class ACMArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("IEEEArticlesHandler")

    def getArticle(self, url):
        self.__logger.error("ACM HANDLER IS NOT IMPLEMENTED YET " + url + " will not be handled")
        return None

    def linkPart(self):
        return "dl.acm.org"

    def name(self):
        return "ACM"

