from ArticlesDataDownloader.IEEE.ieeeHtmlToJson import ieeeHtmlToJson

import selenium
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class IEEEArticlesHandler():
    def __init__(self, driver):
        self.driver = driver

    def getArticle(self, url):
        logging.debug("IEEE::getArticle start " + url)
        try:
            self.driver.get(url)
            logging.debug("Called get for  " + url)

            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id("article"))

            return ieeeHtmlToJson(self.driver.page_source)
        except Exception as error:
            logging.error(error)
            logging.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "ieeexplore.ieee.org/document"

    def name(self):
        return "IEEE"

