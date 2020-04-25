import os
import logging
from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.download_pdf_and_prepare_article_data import download_pdf_and_prepare_article_data
from ArticlesDataDownloader.extract_text_from_pdf import read_pdf_as_json
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.download_utilities import download_file_from_link_to_path


class ACMArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ACMArticlesHandler")

    def get_article(self, url):
        self.__logger.debug("ACM::getArticle start " + url)
        result_data = ArticleData(publisher_link=url)
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_elements_by_xpath("//a[@title='PDF']"))

            self.__logger.info("Wait end")

            python_button = self.driver.find_elements_by_xpath("//a[@title='PDF']")[0]

            link = str(python_button.get_property('href'))

            result_reading = download_pdf_and_prepare_article_data(self.driver, link)
            if result_reading:
                result_data.merge(result_reading)
                result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error('Could not read full text for ' + url)
            result_data.read_status = 'Error while reading article or full text not available'
        return result_data

    def link_part(self):
        return "acm.org"

    def name(self):
        return "ACM"
