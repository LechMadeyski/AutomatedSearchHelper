import json
import logging
import os

from ArticlesDataDownloader.IEEE.IEEEArticlesHandler import IEEEArticlesHandler
from ArticlesDataDownloader.Scopus.ScopusDataDownloader import ScopusDataDownloader
from ArticlesDataDownloader.Willey.WilleyArticlesHandler import WilleyArticlesHandler
from ArticlesDataDownloader.ScienceDirect.ScienceDirectArticlesHandler import ScienceDirectArticlesHandler
from ArticlesDataDownloader.Springer.SpringerArticlesHandler import SpringerArticlesHandler
from ArticlesDataDownloader.ACM.ACMArticlesHandler import ACMArticlesHandler

from ArticlesDataDownloader.getLinkFromDoi import getLinkFromDoi
from ArticlesDataDownloader.getDriver import getDriver
from AutomatedSearchHelperUtilities.getDoiFilename import getDoiFilename, doi_to_filename_base
from ArticlesDataDownloader.RefworksDataDownloader import RefworksDataDownloader


class ArticlesDataDownloader:
    def __init__(self, output_folder, proxy_file=None):
        self.__outputFolder = output_folder
        self.__handlers = None
        self.__logger = logging.getLogger("ArticlesDataDownloader")
        self.__proxyFile = proxy_file
        self.__refworks_downloader = RefworksDataDownloader()
        self.__scopus_downloader = None
        self._driver = None

    def get_doi_filename(self, doi):
        return getDoiFilename(self.__outputFolder, doi)

    def get_doi_filename_and_read_file(self, doi):
        filename = getDoiFilename(self.__outputFolder, doi)
        with open(filename) as json_file:
            return filename, json.load(json_file)

    def write_article_to_file(self, result_data, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_data.doi = doi
        # result_data.merge(self.get_scopus_downloader().get_data(scopus_link))
        result_data.merge(self.__refworks_downloader.get_data(doi))
        result_data.read_status = 'OK'

        with open(filename, "w") as f:
            f.write(json.dumps(result_data.to_dict()))
        return filename, result_data.to_dict()

    def doi_has_result_already(self, doi):
        filename = self.get_doi_filename(doi)
        return os.path.isfile(filename)

    def get_handlers(self):
        if self.__handlers is None:
            if self._driver is None:
                self._driver = getDriver(proxyFile=self.__proxyFile)
            self.__handlers = [
                IEEEArticlesHandler(self._driver),
                WilleyArticlesHandler(self._driver),
                ScienceDirectArticlesHandler(self._driver),
                ACMArticlesHandler(self._driver),
                SpringerArticlesHandler(self._driver),
            ]
        return self.__handlers

    def get_scopus_downloader(self):
        if self.__scopus_downloader is None:
            if self._driver is None:
                self._driver = getDriver(proxyFile=self.__proxyFile)
            self.__scopus_downloader = ScopusDataDownloader(self._driver)
        return self.__scopus_downloader

    def write_incorrect_doi_result(self, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_data = self.get_scopus_downloader().get_data(scopus_link)
        if doi:
            result_data.doi = doi
        result_data.read_status = 'Incorrect doi'
        with open(filename, "w") as f:
            f.write(json.dumps(result_data.to_dict()))
        return filename, result_data.to_dict()

    def write_missing_handler_result(self, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_data = self.get_scopus_downloader().get_data(scopus_link)
        if doi:
            result_data.doi = doi
        result_data.read_status = 'Publisher not supported'
        with open(filename, "w") as f:
            f.write(json.dumps(result_data.to_dict()))
        return filename, result_data.to_dict()

    def write_error_reading_article(self, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_data = self.get_scopus_downloader().get_data(scopus_link)
        if doi:
            result_data.doi = doi
        result_data.read_status = 'Error while reading article or full text not available'
        with open(filename, "w") as f:
            f.write(json.dumps(result_data.to_dict()))
        return filename, result_data.to_dict()


    def readArticle(self, doi, scopus_link, publisher_link=''):
        self.__logger.info("Reading doi : " + doi)
        if self.doi_has_result_already(doi):
            self.__logger.info("Doi " + doi + " already parsed")
            return self.get_doi_filename_and_read_file(doi)

        if not doi and scopus_link:
            # try get data from scopus
            self.write_incorrect_doi_result(doi, scopus_link)

        if not publisher_link:
            publisher_link = str(getLinkFromDoi(doi))

        if not publisher_link:
            self.__logger.error('could not find publisher link for DOI ' + doi)
            return self.write_incorrect_doi_result(doi, scopus_link)

        self.__logger.info("Publisher link is " + str(publisher_link))

        for handler in self.get_handlers():
            self.__logger.debug("Checking " + handler.name() + " with link part " + handler.link_part())
            if handler.link_part() in publisher_link:
                self.__logger.info("Link will be handled by " + handler.name())
                article = handler.get_article(publisher_link)

                if article is None:
                    self.__logger.error("Could not read article")
                    return self.write_error_reading_article(doi, scopus_link)
                else:
                    return self.write_article_to_file(article, doi, scopus_link)
        else:
            self.__logger.error("Could not find handler for " + publisher_link)
            return self.write_missing_handler_result(doi, scopus_link)

    def getDownloadArticles(self, doiList):
        result_filenames = list()
        self.__logger.info("Start downloading articles")
        for doi in doiList:
            filename, resultData = self.readArticle(doi['doi'], doi['scopus_link'])
            result_filenames.append(filename)
        return result_filenames

    def __file_path_from_filename(self, file_name, extension='.json'):
        return self.__outputFolder + '/' + file_name + extension

    def __try_to_read_old_file(self, file_name):
        file_path = self.__file_path_from_filename(file_name)
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                return file_path, json.load(json_file)
        else:
            return None

    def __write_article_data(self, article_data):
        file_path = self.__file_path_from_filename(article_data.filename_base)

        #REFWORKS, SCOPUS
        with open(file_path, "w") as f:
            f.write(json.dumps(article_data.to_dict()))

        return file_path, article_data.to_dict()

    def __fill_article_data_from_other_sources_if_needed(self, article_data):
        if article_data.doi and (not article_data.title or not article_data.authors):
            article_data.merge(self.__refworks_downloader.get_data(article_data.doi))

    def read_article(self, article_data):
        if not article_data.filename_base and article_data.doi:
            article_data.filename_base = doi_to_filename_base(article_data.doi)

        if article_data.filename_base:
            old_file_data =  self.__try_to_read_old_file(article_data.filename_base)
            if old_file_data:
                return old_file_data
        else:
            return None, None

        if not article_data.publisher_link and article_data.doi:
            article_data.publisher_link = getLinkFromDoi(article_data.doi)

        if not article_data.publisher_link and article_data.scopus_link:
            article_data.merge(self.get_scopus_downloader().get_data(article_data.scopus_link))

        if article_data.publisher_link:
            for handler in self.get_handlers():
                self.__logger.debug("Checking " + handler.name() + " with link part " + handler.link_part())
                if handler.link_part() in article_data.publisher_link:
                    self.__logger.info("Link will be handled by " + handler.name())
                    article_data.merge(handler.get_article(article_data.publisher_link))
            else:
                self.__logger.error("Could not find handler for " + article_data.publisher_link)

        self.__fill_article_data_from_other_sources_if_needed(article_data)
        return self.__write_article_data(article_data)








