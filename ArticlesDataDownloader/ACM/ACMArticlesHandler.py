
import selenium
import os
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from .extract_text_from_pdf import read_pdf_as_json
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.download_utilities import download_file_from_link_to_path

class ACMArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ACMArticlesHandler")

    def get_article(self, url):
        self.__logger.debug("ACM::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)

        try:
            self.__logger.debug("Called get for  " + url)
            self.driver.get(url)
            self.__logger.info("Get called")
            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_elements_by_xpath("//a[@title='PDF']"))

            self.__logger.info("Wait end")

            python_button = self.driver.find_elements_by_xpath("//a[@title='PDF']")[0]

            link = str(python_button.get_property('href'))
            output_filename = 'temporary.pdf'
            download_file_from_link_to_path(self.driver, link, output_filename)
            result_reading = ArticleData(text=read_pdf_as_json('temporary.pdf'))
            os.remove('temporary.pdf')
            result_data.merge(result_reading)
            return result_data
        except Exception as error:
            self.__logger.error("ERROR TYPE: " + str(type(error)))
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            os.remove('temporary.pdf')
            return None

    def link_part(self):
        return "dl.acm.org"

    def name(self):
        return "ACM"

