import os
import time

from ArticlesDataDownloader.IEEE.ieee_html_to_json import ieee_html_to_json

import logging
import re
from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.ris_to_article_data import ris_text_to_article_data
from ArticlesDataDownloader.download_utilities import download_pdf, download_file_from_link_that_initiates_download


class IEEEArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("IEEEArticlesHandler")

    def get_article(self, url):
        self.__logger.debug("IEEE::getArticle start " + url)

        self.driver.get(url)
        self.__logger.debug("Called get for  " + url)

        result_data = ArticleData(publisher_link=url)

        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_xpath("//div/strong[contains(text(), 'Abstract')]"))
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("article"))
        except:
            pass

        cite_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//button[contains(text(), 'Cite This') and contains(@class, 'cite-this-btn')]"))
        cite_button.click()

        time.sleep(0.2)


        ris_tab = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[contains(text(), 'RIS') and @class='document-tab-link']"))
        time.sleep(0.2)
        ris_tab.click()

        enable_abstract_checkbox = WebDriverWait(self.driver, 10).until(
            lambda x:  self.driver.find_element_by_xpath("//div[@class='enable-abstract']/input[@type='checkbox']"))
        time.sleep(0.2)
        enable_abstract_checkbox.click()

        ris_text = WebDriverWait(self.driver, 20).until(
            lambda x:  self.driver.find_element_by_xpath("//pre[@class='text ris-text']"))

        result_data.merge(ris_text_to_article_data(ris_text.get_attribute('innerHTML')))

        try:
            WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id("article"))
            result_data.merge(ArticleData(text=ieee_html_to_json(self.driver.page_source)))
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("Could not read html for " + url)
        return result_data


    def download_pdf(self, url):
        id = re.findall("document/(.*?)/", url+'/')[0]
        pdf_link = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?arnumber=' + id

        self.__logger.info('Trying to get pdf from ' + pdf_link)
        return download_file_from_link_that_initiates_download(self.driver, pdf_link)

    def is_applicable(self, url):
        return "ieeexplore.ieee.org" in url

    def name(self):
        return "IEEE"
