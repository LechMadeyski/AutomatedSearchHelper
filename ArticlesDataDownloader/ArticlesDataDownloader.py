import json
import logging
import os

from ArticlesDataDownloader.IEEE.IEEEArticlesHandler import IEEEArticlesHandler
from ArticlesDataDownloader.Willey.WilleyArticlesHandler import WilleyArticlesHandler
from ArticlesDataDownloader.ScienceDirect.ScienceDirectArticlesHandler import ScienceDirectArticlesHandler
from ArticlesDataDownloader.ACM.ACMArticlesHandler import ACMArticlesHandler
from ArticlesDataDownloader.Springer.SpringerArticlesHandler import SpringerArticlesHandler

from ArticlesDataDownloader.getLinkFromDoi import getLinkFromDoi
from ArticlesDataDownloader.getDriver import getDriver
from getDoiFilename import getDoiFilename

from crossref.restful import Works


class ArticlesDataDownloader:
    def __init__(self, output_folder, proxy_file=None):
        self.__outputFolder = output_folder
        self.__handlers = None
        self.__logger = logging.getLogger("ArticlesDataDownloader")
        self.__proxyFile = proxy_file
        self.__works = Works()

    def get_doi_filename(self, doi):
        return getDoiFilename(self.__outputFolder, doi)

    def get_doi_filename_and_read_file(self, doi):
        filename = getDoiFilename(self.__outputFolder, doi)
        with open(filename) as json_file:
            return filename, json.load(json_file)

    def write_article_to_file(self, article, doi):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)

        result_json = dict()
        result_json["doi"] = doi
        result_json["text"] = article

        doi_data = self.__works.doi(doi)
        result_json["publisher"] = doi_data["publisher"]
        result_json["authors"] = doi_data["author"]

        result_json["title"] = ' '.join(doi_data["title"])

        result_json['read_status'] = 'OK'

        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def doi_has_result_already(self, doi):
        filename = self.get_doi_filename(doi)
        return os.path.isfile(filename)

    def get_handlers(self):
        if self.__handlers is None:
            driver = getDriver(proxyFile=self.__proxyFile)
            self.__handlers = [
                IEEEArticlesHandler(driver),
                WilleyArticlesHandler(driver),
                ScienceDirectArticlesHandler(driver),
                # ACMArticlesHandler(driver),
                SpringerArticlesHandler(driver),
            ]
        return self.__handlers

    def write_incorrect_doi_result(self, doi):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_json = dict()
        result_json["doi"] = doi
        result_json["text"] = dict()

        result_json["publisher"] = 'unknown'
        result_json["authors"] = 'unknown'

        result_json["title"] = 'unknown'
        result_json["read_status"] = 'ERROR READING DOI DATA'
        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def write_missing_handler_result(self, doi):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_json = dict()
        result_json["doi"] = doi
        result_json["text"] = dict()

        result_json["publisher"] = 'unknown'
        result_json["authors"] = 'unknown'

        result_json["title"] = 'unknown'

        result_json["read_status"] = 'NO HANDLER IMPLEMENTED'
        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def write_error_reading_article(self, doi):
        filename = self.get_doi_filename(doi)
        self.__logger.info("Writing article to " + filename)
        result_json = dict()
        result_json["doi"] = doi
        result_json["text"] = dict()

        doi_data = self.__works.doi(doi)
        result_json["publisher"] = doi_data["publisher"]
        result_json["authors"] = doi_data["author"]
        result_json["title"] = ' '.join(doi_data["title"])

        result_json["read_status"] = 'ERROR READING ARTICLE'
        with open(filename, "w") as f:
            f.write(json.dumps(result_json))
        return filename, result_json

    def readArticle(self, doi):
        if self.doi_has_result_already(doi):
            self.__logger.info("Doi " + doi + " already parsed")
            return self.get_doi_filename_and_read_file(doi)

        self.__logger.info("Reading doi : " + doi)
        real_link = getLinkFromDoi(doi)
        if real_link is None:
            self.__logger.error("Could not find link from doi")
            return self.write_incorrect_doi_result(doi)

        self.__logger.info("Real link is " + real_link)

        for handler in self.get_handlers():
            self.__logger.debug("Checking " + handler.name() + " with link part " + handler.linkPart())
            if handler.linkPart() in real_link:
                self.__logger.info("Link will be handled by " + handler.name())
                article = handler.getArticle(real_link)

                if article is None:
                    self.__logger.error("Could not read article")
                    return self.write_error_reading_article(doi)
                else:
                    return self.write_article_to_file(article, doi)
        else:
            self.__logger.error("Could not find handler for " + real_link)
            return self.write_missing_handler_result(doi)

    def getDownloadArticles(self, doiList):
        result_filenames = list()
        self.__logger.info("Start downloading articles")
        for doi in doiList:
            filename, resultData = self.readArticle(doi)
            if resultData['read_status'] == 'OK':
                result_filenames.append(filename)
        return result_filenames

    def getDownloadArticles2(self, doiList):
        self.__logger.info("Start downloading articles")

        result_filenames = list()
        handler_not_found_count = 0
        error_occured_count = 0
        for doi in doiList:
            if self.doi_has_result_already(doi):
                self.__logger.info("Doi " + doi + " already parsed")
                result_filenames.append(self.get_doi_filename(doi))
                continue

            self.__logger.info("Reading doi : " + doi)
            real_link = getLinkFromDoi(doi)
            if real_link is None:
                self.__logger.error("Could not find link from doi")
                continue

            self.__logger.info("Real link is " + real_link)

            for handler in self.get_handlers():
                self.__logger.debug("Checking " + handler.name() + " with link part " + handler.linkPart())
                if handler.linkPart() in real_link:
                    self.__logger.info("Link will be handled by " + handler.name())
                    article = handler.getArticle(real_link)

                    if article is None:
                        self.__logger.error("Could not read article")
                        error_occured_count += 1
                    else:
                        result_filename, _ = self.write_article_to_file(article, doi)
                        result_filenames.append(result_filename)
                    break
            else:
                self.__logger.error("Could not find handler for " + real_link)
                handler_not_found_count += 1
            self.__logger.info("Doi reading finished")

        self.__logger.info(
            "Finished analysing articles total analyzed : " + str(len(doiList)) \
            + " successful :" + str(len(result_filenames)) \
            + " handler not found : " + str(handler_not_found_count) \
            + " error occured " + str(error_occured_count))

        return result_filenames
