import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.Springer.springer_html_to_article_data import springer_html_to_article_data
from ArticlesDataDownloader.ris_to_article_data import ris_to_article_data
from ArticlesDataDownloader.download_utilities import wait_for_file_download, wait_until_all_files_downloaded
import os
import time
from ArticlesDataDownloader.download_utilities import download_file_from_link_to_path

class SpringerArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("SpringerArticlesHandler")

    def get_article(self, url):
        self.__logger.debug("Springer::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)
        url_to_ris = url.replace('http://link.springer.com/', 'https://citation-needed.springer.com/v2/references/')+ \
                     '?format=refman&flavour=citation'
        self.driver.get(url_to_ris)
        filename = url.replace('http://link.springer.com/', '').replace('/', '_') + '.ris'

        self.__logger.debug('Trying to ger article data from', filename)
        if wait_for_file_download(filename):
            self.__logger.debug('File downloaded successfully - reading data')
            result_data.merge(ris_to_article_data(filename))
            os.remove(filename)
        else:
            self.__logger.warning('Could not download ris file for ' + url)

        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)
            result_data.merge(springer_html_to_article_data(self.driver.page_source))
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            result_data.read_status = 'Error while reading article or full text not available'

        return result_data


    def link_part(self):
        return "link.springer.com"

    def is_applicable(self, url):
        return self.link_part() in url

    def name(self):
        return "Springer"

