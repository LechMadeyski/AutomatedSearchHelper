import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.Springer.springer_html_to_article_data import springer_html_to_article_data
from ArticlesDataDownloader.ris_to_article_data import ris_to_article_data

from ArticlesDataDownloader.download_file_from_link_to_path import download_file_from_link_to_path

class SpringerArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("SpringerArticlesHandler")

    def getArticle(self, url):
        self.__logger.debug("Springer::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)


        url_to_ris = url.replace('http://link.springer.com/', 'https://citation-needed.springer.com/v2/references/')+ \
                     '?format=refman&flavour=citation'
        self.driver.get(url_to_ris)
        filename = url.replace('http://link.springer.com/', '').replace('/', '_') +'.ris'
        print(self.driver.page_source)

        self.__logger.debug('Trying to ger article data from', filename)

        result_data.merge(ris_to_article_data(filename))

        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)

            # element = WebDriverWait(self.driver, 10).until(
            #     lambda x: x.find_element_by_id("article"))

            result_data.merge(springer_html_to_article_data(self.driver.page_source))
            return result_data
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "link.springer.com"

    def name(self):
        return "Springer"

