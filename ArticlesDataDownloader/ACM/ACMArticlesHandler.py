import os
import logging
from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.download_pdf_and_prepare_article_data import download_pdf

from ArticlesDataDownloader.ArticleData import ArticleData


class ACMArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ACMArticlesHandler")

    def get_article(self, url):
        return ArticleData(publisher_link=url)

    def download_pdf(self, url):
        self.__logger.debug("ACM::download_pdf start " + url)
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_xpath("//a[@title='PDF']"))
        self.__logger.info("Wait end")
        python_button = self.driver.find_elements_by_xpath("//a[@title='PDF']")[0]
        link = str(python_button.get_property('href'))
        PDF_FILENAME = 'ACM_temporary.pdf'
        return download_pdf(self.driver, link, PDF_FILENAME)


    def is_applicable(self, url):
        return "acm.org" in url

    def name(self):
        return "ACM"
