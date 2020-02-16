from ArticlesDataDownloader.IEEE.ieeeHtmlToJson import ieeeHtmlToJson

import selenium
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class IEEEArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("IEEEArticlesHandler")

    def getArticle(self, url):
        self.__logger.debug("IEEE::getArticle start " + url)
        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)

            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id("article"))

            return ieeeHtmlToJson(self.driver.page_source)
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "ieeexplore.ieee.org"

    def name(self):
        return "IEEE"

