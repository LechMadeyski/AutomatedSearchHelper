from ArticlesDataDownloader.Willey.willeyHtmlToJson import willeyHtmlToJson

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
            result = willeyHtmlToJson(self.driver.page_source)
            return result
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "doi.wiley.com/"

    def name(self):
        return "Willey"
