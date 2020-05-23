from ArticlesDataDownloader.Willey.willey_html_to_json import willey_html_to_json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.bib_to_article_data import bib_text_to_article_data
from ArticlesDataDownloader.download_utilities import download_pdf, download_file_from_link_that_initiates_download
import logging

from ArticlesDataDownloader.ris_to_article_data import ris_text_to_article_data


class WilleyArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("WilleyArticlesHandler")

    def __get_reference_text_with_given_radio_type(self, url, reference_radio_name):
        self.driver.get(url)
        tools_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[@class='article-tools__ctrl']"))
        tools_button.click()

        list_buttons = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_elements_by_xpath("//li[@class='article-tool']/a"))

        citation_button = [x for x in list_buttons if 'Export citation' in x.get_attribute('innerHTML')][0]
        citation_button.click()

        radio_labels = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_elements_by_xpath("//label[@class='radio--primary']"))
        citation_type_radio = [x for x in radio_labels if reference_radio_name in x.get_attribute('innerHTML')][0]
        citation_type_radio.click()

        radio_labels = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_elements_by_xpath("//label[@class='radio--primary' and @for='other-type']"))

        indirect_radio = [x for x in radio_labels if 'Indirect import' in x.get_attribute('innerHTML')][0]
        indirect_radio.click()
        download_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//input[@value='Download']"))
        download_button.click()
        pre = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//pre"))
        return pre.get_attribute('innerHTML')

    def __try_reading_data_from_ris(self, url):
        return ris_text_to_article_data(self.__get_reference_text_with_given_radio_type(url, 'RIS'))

    def __try_reading_data_from_bib(self, url):
        return bib_text_to_article_data(self.__get_reference_text_with_given_radio_type(url, 'BibTex'))

    def __try_download_text_from_html(self, url):
        self.driver.get(url)
        self.__logger.debug("Called get for  " + url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "article-section__content"))
        )
        return ArticleData(text=willey_html_to_json(self.driver.page_source))

    def get_article(self, url):
        self.__logger.debug("Willey::getArticle start " + url)
        result_data = ArticleData(publisher_link=url)
        try:
            result_data.merge(self.__try_reading_data_from_ris(url))
        except Exception as e:
            self.__logger.debug("Willey::failed to load ris for " + url)
            self.__logger.exception(e)
            try:
                result_data.merge(self.__try_reading_data_from_bib(url))
            except Exception as e:
                self.__logger.debug("Willey::failed to load bib for " + url)
                self.__logger.exception(e)
                result_data.read_status = 'Failed to download bibliographic information'
        try:
            result_data.merge(self.__try_download_text_from_html(url))
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error("some error occured, could not read full article text for " + url)
            self.__logger.exception(error)
            result_data.read_status = 'Error while reading article or full text not available'

        result_data.merge(ArticleData(publisher='John Wiley & Sons, Ltd'))
        return result_data

    def download_pdf(self, url):
        pdf_link = url.replace('doi/abs', 'doi/pdfdirect')\
                       .replace('doi/full', 'doi/pdfdirect')\
                       .replace('http:', 'https:')\
                       .replace('doi.wiley.com', 'onlinelibrary.wiley.com/doi/pdfdirect') + '?download=true'
        self.__logger.info('Trying to download pdf from ' + pdf_link)
        return download_file_from_link_that_initiates_download(self.driver, pdf_link)

    def is_applicable(self, url):
        return "wiley.com" in url

    def name(self):
        return "Willey"
