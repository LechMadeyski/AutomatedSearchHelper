from ArticlesDataDownloader.Willey.willeyHtmlToJson import willeyHtmlToJson
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class WilleyArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("WilleyArticlesHandler")

    def getArticle(self, url):
        self.__logger.debug("Willey::getArticle start " + url)
        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "article-section__content"))
            )
            result = willeyHtmlToJson(self.driver.page_source)
            return result
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "wiley.com"

    def name(self):
        return "Willey"
