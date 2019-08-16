from ArticlesDataDownloader.ScienceDirect.scienceDirectHtmlToJson import scienceDirectHtmlToJson

import selenium
import logging
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class ScienceDirectArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ScienceDirectArticlesHandler")

    def getArticle(self, url):

        url = url.replace("linkinghub.elsevier.com/retrieve/", "sciencedirect.com/science/article/")
        self.__logger.info("Url changed to " + url)
        self.__logger.debug("ScienceDirect::getArticle start " + url)
        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)

            def ready(x):
                found = False
                try:
                    x.find_element_by_id("sec0001")
                    found = True
                except:
                    pass
                try:
                    x.find_element_by_id("s0005")
                    found = True
                except:
                    pass
                return found

            WebDriverWait(self.driver, 20).until(ready)

            return scienceDirectHtmlToJson(self.driver.page_source)

        except Exception as error:
            self.__logger.error(str(error))
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "linkinghub.elsevier.com"

    def name(self):
        return "ScienceDirect"
