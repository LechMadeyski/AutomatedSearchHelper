import os

from ArticlesDataDownloader.ScienceDirect.science_direct_html_to_json import science_direct_html_to_json

import re
import logging
from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.download_pdf_and_prepare_article_data import download_pdf_and_prepare_article_data
from ArticlesDataDownloader.download_utilities import wait_until_all_files_downloaded, wait_for_file_download, \
    clear_download_directory, get_files_from_download_directory, download_pdf, \
    download_file_from_link_that_initiates_download
from ArticlesDataDownloader.ris_to_article_data import ris_to_article_data
import time

def article_ready(x):
    found = False
    try:
        x.find_element_by_id("body")
        found = True
    except:
        pass
    try:
        x.find_element_by_id("s0005")
        found = True
    except:
        pass
    return found

class ScienceDirectArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ScienceDirectArticlesHandler")

    def get_article(self, url):
        url = url.replace("linkinghub.elsevier.com/retrieve/", "sciencedirect.com/science/article/")
        self.__logger.info("Url changed to " + url)
        self.__logger.debug("ScienceDirect::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)

        clear_download_directory()

        self.driver.get(url)

        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@id='popover-trigger-export-citation-popover']/button/span"))

        export_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element_by_xpath("//div[@id='popover-trigger-export-citation-popover']/button"))
        time.sleep(1)
        export_button.click()


        ris_download_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element_by_xpath("//button[@aria-label='ris']"))

        ris_download_button.click()
        time.sleep(1) # wait until download initiated
        wait_until_all_files_downloaded(self.driver)
        downloaded_files = get_files_from_download_directory()

        if len(downloaded_files) == 1:
            self.__logger.debug('File downloaded successfully - reading data')
            result_data.merge(ris_to_article_data(downloaded_files[0]))
            clear_download_directory()

        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)
            WebDriverWait(self.driver, 20).until(article_ready)
            result_data.merge(ArticleData(text=science_direct_html_to_json(self.driver.page_source)))
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error(str(error))
            self.__logger.error("Could not read html text for " + url)

        return result_data


    def download_pdf(self, url):
        id = re.findall("/pii/(.*?)/", url + '/')[0]
        pdf_link = 'https://www.sciencedirect.com/science/article/pii/%s/pdfft?isDTMRedir=true&download=true' % id
        self.__logger.info('Trying to get pdf from ' + pdf_link)
        return download_file_from_link_that_initiates_download(self.driver, pdf_link)

    def is_applicable(self, url):
        for link_part in ['linkinghub.elsevier.com', 'sciencedirect.com']:
            if link_part in url:
                return True
        return False


    def name(self):
        return "ScienceDirect"
