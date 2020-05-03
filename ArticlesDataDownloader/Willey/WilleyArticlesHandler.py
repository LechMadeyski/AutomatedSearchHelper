from ArticlesDataDownloader.Willey.willey_html_to_json import willey_html_to_json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.download_pdf_and_prepare_article_data import download_pdf
from ArticlesDataDownloader.ris_to_article_data import ris_text_to_article_data
import logging


class WilleyArticlesHandler:
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("WilleyArticlesHandler")

    def get_article(self, url):
        self.__logger.debug("Willey::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)
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
        ris_radio = [x for x in radio_labels if 'RIS' in x.get_attribute('innerHTML')][0]
        ris_radio.click()

        radio_labels = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_elements_by_xpath("//label[@class='radio--primary' and @for='other-type']"))

        indirect_radio = [x for x in radio_labels if 'Indirect import' in x.get_attribute('innerHTML')][0]
        indirect_radio.click()

        download_button = WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//input[@value='Download']"))
        download_button.click()

        pre = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//pre"))
        result_data.merge(ris_text_to_article_data(pre.get_attribute('innerHTML')))

        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "article-section__content"))
            )
            result_data.merge(ArticleData(
                text=willey_html_to_json(self.driver.page_source)))
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error(error)
            self.__logger.error("some error occured, could not read full article text for " + url)
            result_data.read_status = 'Error while reading article or full text not available'

        return result_data

    def download_pdf(self, url):
        pdf_link = url.replace('doi/abs', 'doi/pdfdirect')\
                       .replace('doi/full', 'doi/pdfdirect')\
                       .replace('http:', 'https:')\
                       .replace('doi.wiley.com', 'onlinelibrary.wiley.com/doi/pdfdirect') + '?download=true'
        PDF_FILENAME = 'WILLEY_temporary.pdf'


        self.__logger.info('Trying to download pdf from ' + pdf_link)

        return download_pdf(self.driver, pdf_link, PDF_FILENAME)

    def is_applicable(self, url):
        return "wiley.com" in url

    def name(self):
        return "Willey"
