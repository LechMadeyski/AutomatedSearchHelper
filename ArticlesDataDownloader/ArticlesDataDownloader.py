import json
import logging
import os

from ArticlesDataDownloader.IEEE.IEEEArticlesHandler import IEEEArticlesHandler
from ArticlesDataDownloader.ScopusDataDownloader import ScopusDataDownloader
from ArticlesDataDownloader.Willey.WilleyArticlesHandler import WilleyArticlesHandler
from ArticlesDataDownloader.ScienceDirect.ScienceDirectArticlesHandler import ScienceDirectArticlesHandler
from ArticlesDataDownloader.Springer.SpringerArticlesHandler import SpringerArticlesHandler

from ArticlesDataDownloader.getLinkFromDoi import getLinkFromDoi
from ArticlesDataDownloader.getDriver import getDriver
from AutomatedSearchHelperUtilities.getDoiFilename import getDoiFilename

from crossref.restful import Works


class ArticlesDataDownloader:
    def __init__(self, output_folder, proxy_file=None):
        self.__outputFolder = output_folder
        self.__handlers = None
        self.__logger = logging.getLogger("ArticlesDataDownloader")
        self.__proxyFile = proxy_file
        self.__works = Works()
        self.__scopus_downloader = None
        self._driver = None

    def get_doi_filename(self, doi):
        return getDoiFilename(self.__outputFolder, doi)

    def get_doi_filename_and_read_file(self, doi):
        filename = getDoiFilename(self.__outputFolder, doi)
        with open(filename) as json_file:
            return filename, json.load(json_file)

    def write_article_to_file(self, article, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)

        result_json = self.get_scopus_downloader().get_data(scopus_link)
        result_json["doi"] = doi
        result_json["text"] = article

        try:
            doi_data = self.__works.doi(doi)
            result_json["publisher"] = doi_data.get("publisher", str())
            result_json["authors"] = [x.get('given', str()) + ' ' + x.get('family', str()) for x in doi_data.get("author", [])]
            result_json["title"] = ' '.join(doi_data.get("title", str()))
            result_json['read_status'] = 'OK'
        except:
            self.__logger.error("some error while reading doi data")
            pass

        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

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
                # ACMArticlesHandler(self._driver),
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
        result_json = self.get_scopus_downloader().get_data(scopus_link)
        if doi:
            result_json["doi"] = doi
        result_json["read_status"] = 'ERROR READING DOI DATA'
        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def write_missing_handler_result(self, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_json = self.get_scopus_downloader().get_data(scopus_link)
        if doi:
            result_json["doi"] = doi
        result_json["read_status"] = 'NO HANDLER IMPLEMENTED'
        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def write_error_reading_article(self, doi, scopus_link):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_json = self.get_scopus_downloader().get_data(scopus_link)
        if doi:
            result_json["doi"] = doi

        result_json["read_status"] = 'ERROR READING ARTICLE'
        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def readArticle(self, doi, scopus_link):
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
            self.__logger.debug("Checking " + handler.name() + " with link part " + handler.linkPart())
            if handler.linkPart() in real_link:
                self.__logger.info("Link will be handled by " + handler.name())
                article = handler.getArticle(real_link)

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

