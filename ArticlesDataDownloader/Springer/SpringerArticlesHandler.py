import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.Springer.springer_html_to_article_data import springer_html_to_article_data
from ArticlesDataDownloader.download_pdf_and_prepare_article_data import download_pdf
from ArticlesDataDownloader.ris_to_article_data import ris_to_article_data
from ArticlesDataDownloader.download_utilities import wait_for_file_download, wait_until_all_files_downloaded, \
    download_file_from_link_that_initiates_download, clear_download_directory
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

        self.__logger.debug('Trying to read ris data from ' + url_to_ris)
        downloaded_file = download_file_from_link_that_initiates_download(self.driver, url_to_ris)
        if downloaded_file:
            self.__logger.debug('Trying to ger article data from', downloaded_file)
            result_data.merge(ris_to_article_data(downloaded_file))
            clear_download_directory()
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


    def download_pdf(self, url):
        pdf_link = url.replace('chapter', 'content/pdf')\
                       .replace('book', 'content/pdf') + '.pdf'

        self.__logger.info('Trying to download pdf from ' + pdf_link)

        return download_file_from_link_that_initiates_download(self.driver, pdf_link)

    def is_applicable(self, url):
        return self.link_part() in url

    def name(self):
        return "Springer"

