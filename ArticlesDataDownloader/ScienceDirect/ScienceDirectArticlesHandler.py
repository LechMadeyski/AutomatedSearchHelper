from ArticlesDataDownloader.ScienceDirect.scienceDirectHtmlToJson import scienceDirectHtmlToJson

import selenium
import logging
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class ScienceDirectArticlesHandler():
    def __init__(self, driver):
        self.driver = driver

    def getArticle(self, url):

        url = url.replace("linkinghub.elsevier.com/retrieve/", "sciencedirect.com/science/article/")
        logging.info("Url changed to " + url)
        logging.debug("ScienceDirect::getArticle start " + url)
        try:
            self.driver.get(url)
            logging.debug("Called get for  " + url)
            element = WebDriverWait(self.driver, 20).until(
                lambda x: x.find_element_by_id("sec1"))
            return scienceDirectHtmlToJson(self.driver.page_source)

        except Exception as error:
            logging.error(str(error))
            logging.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "linkinghub.elsevier.com"

    def name(self):
        return "ScienceDirect"

