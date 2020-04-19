import os

from ArticlesDataDownloader.ACM.extract_text_from_pdf import read_pdf_as_json

from ArticlesDataDownloader.IEEE.ieeeHtmlToJson import ieeeHtmlToJson

import logging
import re
from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.ris_to_article_data import ris_text_to_article_data
from ArticlesDataDownloader.download_utilities import download_file_from_link_to_path

class IEEEArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("IEEEArticlesHandler")

    def get_article(self, url):
        self.__logger.debug("IEEE::getArticle start " + url)

        self.driver.get(url)
        self.__logger.debug("Called get for  " + url)

        result_data = ArticleData(publisher_link=url)

        cite_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//button[contains(text(), 'Cite This')]"))
        cite_button.click()

        ris_tab = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[contains(text(), 'RIS')]"))
        ris_tab.click()

        enable_abstract_checkbox = WebDriverWait(self.driver, 10).until(
            lambda x:  self.driver.find_element_by_xpath("//div[@class='enable-abstract']/input[@type='checkbox']"))
        enable_abstract_checkbox.click()

        ris_text = WebDriverWait(self.driver, 10).until(
            lambda x:  self.driver.find_element_by_xpath("//pre[@class='text ris-text']"))

        result_data.merge(ris_text_to_article_data(ris_text.get_attribute('innerHTML')))

        try:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("article"))

            result_data.merge(ArticleData(text=ieeeHtmlToJson(self.driver.page_source)))
            return result_data
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("Could not read html for " + url)
            self.__logger.info("Trying to read from pdf")

            # self.driver.get(url)

            # pdf_button = WebDriverWait(self.driver, 10).until(
            #     lambda x: x.find_element_by_xpath("//a[contains(@class, 'stats-document-lh-action-downloadPdf_2')]/span"))

            # pdf_button = WebDriverWait(self.driver, 10).until(
            #     lambda x: x.find_element_by_xpath("//span[contains(text(), 'PDF')]"))
            #
            #
            # pdf_button.click()


            try:
                id = re.findall("document/(.*?)/", url+'/')[0]

                pdf_link = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?arnumber=' + id

                self.__logger.info('Trying to get pdf from ' + pdf_link)

                output_filename = 'temporary.pdf'

                download_file_from_link_to_path(self.driver, pdf_link, output_filename)
                result_reading = ArticleData(text=read_pdf_as_json('temporary.pdf'))
                os.remove('temporary.pdf')
                result_data.merge(result_reading)
                return result_data
            except:
                self.__logger.error('Failed to read from pdf')

                return None

    def link_part(self):
        return "ieeexplore.ieee.org"

    def name(self):
        return "IEEE"
