from ArticlesDataDownloader.Willey.willeyHtmlToJson import willeyHtmlToJson

import logging

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

class WilleyArticlesHandler:
    def __init__(self, driver):
        self.driver = driver

    def getArticle(self, url):
        logging.debug("Willey::getArticle start " + url)
        try:
            self.driver.get(url)
            logging.debug("Called get for  " + url)
            result = willeyHtmlToJson(self.driver.page_source)
            return result
        except Exception as error:
            logging.error(error)
            logging.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "doi.wiley.com/"

    def name(self):
        return "Willey"
