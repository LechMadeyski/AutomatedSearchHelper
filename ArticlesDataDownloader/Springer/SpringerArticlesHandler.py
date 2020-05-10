import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.Springer.springer_html_to_article_data import springer_html_to_article_data
from ArticlesDataDownloader.pdf_utilities import extract_given_pages_from_pdf
from ArticlesDataDownloader.ris_to_article_data import ris_to_article_data
from ArticlesDataDownloader.download_utilities import download_file_from_link_that_initiates_download,\
    clear_download_directory, download_file_from_click_of_button
import os
import time
from ArticlesDataDownloader.download_utilities import download_file_from_link_to_path

class SpringerArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("SpringerArticlesHandler")

    def __citation_file_to_article_data(self, citation_file):
        if citation_file:
            self.__logger.debug('Trying to ger article data from', citation_file)
            result = ris_to_article_data(citation_file)
            clear_download_directory()
            return result
        else:
            raise Exception("cannot read citation for " + self.driver.current_url)

    def __get_article_data_from_chapter(self):
        self.__logger.info('Analyzing article as chapter')
        download_citation_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[contains(@data-track-label, 'RIS')]"))
        citation_link = download_citation_button.get_attribute('href')
        self.__logger.info('Got link to ris ' + citation_link)
        downloaded_file = download_file_from_link_that_initiates_download(self.driver, citation_link)
        return self.__citation_file_to_article_data(downloaded_file)

    def __get_article_data_from_article(self):
        self.__logger.info('Analyzing article as articles')
        download_citation_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[contains(@data-track-action, 'download article citation')]"))
        citation_link = download_citation_button.get_attribute('href')
        self.__logger.info('Got link to ris ' + citation_link)
        downloaded_file = download_file_from_link_that_initiates_download(self.driver, citation_link)
        return self.__citation_file_to_article_data(downloaded_file)

    def get_article(self, url):
        self.__logger.debug("Springer::getArticle start " + url)

        self.driver.get(url)


        self.__logger.info('got url ' + self.driver.current_url)
        result_data = ArticleData(publisher_link=self.driver.current_url)

        downloaded_file = str()
        if '/chapter/' in self.driver.current_url:
            result_data.merge(self.__get_article_data_from_chapter())
        elif '/article' in self.driver.current_url:
            result_data.merge(self.__get_article_data_from_article())
        else:
            result_data.read_status = 'Only article or chapter types are supported for Springer'
            return result_data

        try:
            self.__logger.debug("Called get for  " + url)
            result_data.text = springer_html_to_article_data(self.driver.page_source).text
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            result_data.read_status = 'Error while reading article or full text not available'

        return result_data




    def download_pdf(self, url):
        self.driver.get(url)

        self.__logger.info('got url for pdf ' + self.driver.current_url)

        if '/chapter/' in self.driver.current_url:
            self.__logger.info('Trying to get pdf from chapter')
            download_pdf_button = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[contains(@data-track-action, 'Pdf download')]"))
            pdf_link = download_pdf_button.get_attribute('href')
            return download_file_from_link_that_initiates_download(self.driver, pdf_link)
        elif '/article' in self.driver.current_url:
            self.__logger.info('Trying to get pdf from chapter')
            download_pdf_button = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[contains(@class, 'c-pdf-download__link')]"))
            pdf_link = download_pdf_button.get_attribute('href')
            return download_file_from_link_that_initiates_download(self.driver, pdf_link)
        else:
            return str()

    def is_applicable(self, url):
        return "link.springer.com" in url or "springeropen.com" in url

    def name(self):
        return "Springer"

