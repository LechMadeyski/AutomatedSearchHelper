from ArticlesDataDownloader.ScienceDirect.scienceDirectHtmlToJson import scienceDirectHtmlToJson

import selenium
import logging
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData

##RIS EXAMPLE LINK https://www.sciencedirect.com/sdfe/arp/cite?pii=S0020025519308242&format=application%2Fx-research-info-systems&withabstract=false

def article_ready(x):
    found = False
    try:
        x.find_element_by_id("body")
        found = True
    except:
        pass
    try:
        x.find_element_by_id("s0005")
        found = True
    except:
        pass
    return found

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
            WebDriverWait(self.driver, 20).until(article_ready)
            return ArticleData(text = scienceDirectHtmlToJson(self.driver.page_source))
        except Exception as error:
            self.__logger.error(str(error))
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "linkinghub.elsevier.com"

    def name(self):
        return "ScienceDirect"
