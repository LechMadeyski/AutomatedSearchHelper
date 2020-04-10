import json
import logging
import os

from ArticlesDataDownloader.IEEE.IEEEArticlesHandler import IEEEArticlesHandler
from ArticlesDataDownloader.ScopusDataDownloader import ScopusDataDownloader
from ArticlesDataDownloader.Willey.WilleyArticlesHandler import WilleyArticlesHandler
from ArticlesDataDownloader.ScienceDirect.ScienceDirectArticlesHandler import ScienceDirectArticlesHandler
from ArticlesDataDownloader.Springer.SpringerArticlesHandler import SpringerArticlesHandler
from ArticlesDataDownloader.ACM.ACMArticlesHandler import ACMArticlesHandler

from ArticlesDataDownloader.getLinkFromDoi import getLinkFromDoi
from ArticlesDataDownloader.getDriver import getDriver
from AutomatedSearchHelperUtilities.getDoiFilename import getDoiFilename
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
        result_data.merge(self.get_scopus_downloader().get_data(scopus_link))
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

    def readArticle(self, doi, scopus_link):
        # if DOI NOT EMPTY
            # Save scopus link
            # Get link from doi
        # if link empty and scopus link empty
            # save incorrect
        # for handler in handlers
            # if link part matchers
                # get filename for link/doi
                # try reading filename
                    # if successful
                        # save
                    # else
                        # Try reading data
                        # if success ->
                            # save
                        # Else
                            # save read error
                        # break
        # if scopus link
            # Get data from scopus
            # if article has data
                # merge
            # else
                # save scopus

        if self.doi_has_result_already(doi):
            self.__logger.info("Doi " + doi + " already parsed")
            return self.get_doi_filename_and_read_file(doi)

        self.__logger.info("Reading doi : " + doi)
        real_link = str(getLinkFromDoi(doi))
        if real_link is None:
            self.__logger.error("Could not find link from doi")
            return self.write_incorrect_doi_result(doi, scopus_link)

        self.__logger.info("Real link is " + str(real_link))

        for handler in self.get_handlers():
            self.__logger.debug("Checking " + handler.name() + " with link part " + handler.link_part())
            if handler.link_part() in real_link:
                self.__logger.info("Link will be handled by " + handler.name())
                article = handler.get_article(real_link)

                if article is None:
                    self.__logger.error("Could not read article")
                    return self.write_error_reading_article(doi, scopus_link)
                else:
                    return self.write_article_to_file(article, doi, scopus_link)
        else:
            self.__logger.error("Could not find handler for " + real_link)
            return self.write_missing_handler_result(doi, scopus_link)

    def getDownloadArticles(self, doiList):
        result_filenames = list()
        self.__logger.info("Start downloading articles")
        for doi in doiList:
            filename, resultData = self.readArticle(doi['doi'], doi['scopus_link'])
            result_filenames.append(filename)
        return result_filenames
