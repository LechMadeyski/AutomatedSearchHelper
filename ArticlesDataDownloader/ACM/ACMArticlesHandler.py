import os
import logging
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.bib_to_article_data import bib_to_article_datas_with_ids
from ArticlesDataDownloader.download_utilities import download_pdf, download_file_from_click_of_button
from ArticlesDataDownloader.text_utilities import format_text_and_split_into_sentences


class ACMArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ACMArticlesHandler")

    def get_article(self, url):
        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[contains(@class, 'abstractSection abstractInFull')]"))
        abstract_paragraphs = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_elements_by_xpath("//div[contains(@class, 'abstractSection abstractInFull')]/p"))
        text = [dict(title='Abstract', paragraphs=[
            dict(sentences=format_text_and_split_into_sentences(
                par.get_attribute('innerHTML'))) for par in abstract_paragraphs])]
        result = ArticleData(publisher_link=url, text=text, read_status='Full text not avaliable')

        cite_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[@data-title='Export Citation']"))

        desired_y = (cite_button.size['height'] / 2) + cite_button.location['y']
        window_h = self.driver.execute_script('return window.innerHeight')
        window_y = self.driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


        cite_button.click()

        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@class='csl-right-inline']"))

        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[@title='Download citation']/i[@class='icon-Icon_Download']"))

        download_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[@title='Download citation']"))

        downloaded_bibs = download_file_from_click_of_button(self.driver, download_button)
        if downloaded_bibs:
            article_datas = bib_to_article_datas_with_ids(downloaded_bibs)
            if len(article_datas) == 1:
                result.merge(article_datas[0][1])
            else:
                result.read_status = 'Failed reading bibliographic information'
        else:
            result.read_status = 'Failed downloading bibliographic information'
        return result


    def download_pdf(self, url):
        try:
            self.__logger.debug("ACM::download_pdf start " + url)
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(lambda x: x.find_elements_by_xpath("//a[@title='PDF']"))
            self.__logger.info("Wait end")
            python_button = self.driver.find_elements_by_xpath("//a[@title='PDF']")[0]
            link = str(python_button.get_property('href'))
            PDF_FILENAME = 'ACM_temporary.pdf'
            return download_pdf(self.driver, link, PDF_FILENAME)
        except:
            return str()

    def is_applicable(self, url):
        return "acm.org" in url

    def name(self):
        return "ACM"
