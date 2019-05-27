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


class ArticlesDataDownloader:
    def __init__(self, outputFolder, proxyFile = None):
        self.__outputFolder = outputFolder
        self.__handlers = None
        self.__logger = logging.getLogger("ArticlesDataDownloader")
        self.__proxyFile = proxyFile

    def getDoiFilename(self, doi):
        return getDoiFilename(self.__outputFolder, doi)

    def writeArticleToFile(self, article, doi):
        filename = self.getDoiFilename(doi)
        self.__logger.info("Writing article to "+ filename)
        f = open(filename, "w")
        f.write(json.dumps({"doi": doi, "text":article}))
        return filename

    def doiHasResultAlready(self, doi):
        filename = self.getDoiFilename(doi)
        return os.path.isfile(filename)

    def getHandlers(self):
        if self.__handlers is None:
            driver = getDriver(proxyFile = self.__proxyFile)
            self.__handlers = [
                IEEEArticlesHandler(driver),
                WilleyArticlesHandler(driver),
                ScienceDirectArticlesHandler(driver),
                ACMArticlesHandler(driver),
                SpringerArticlesHandler(driver),
            ]
        return self.__handlers

    def getDownloadArticles(self, doiList):
        self.__logger.info("Start downloading articles")

        resultFilenames = list()

        for doi in doiList:
            if self.doiHasResultAlready(doi):
                self.__logger.info("Doi " + doi + " already parsed")
                resultFilenames.append(self.getDoiFilename(doi))
                continue

            self.__logger.info("Reading doi : " + doi)
            realLink = getLinkFromDoi(doi)
            if doi is None:
                self.__logger.error("Could not find link from doi")
                continue;
            self.__logger.info ("Real link is " + realLink)

            for handler in self.getHandlers():
                self.__logger.debug("Checking " + handler.name() + " with link part "+ handler.linkPart() )
                if handler.linkPart() in realLink:
                    self.__logger.info("Link will be handled by " + handler.name())
                    article = handler.getArticle(realLink)

                    if article is None:
                        self.__logger.error("Could not read article")
                    else:
                        resultFilename = self.writeArticleToFile(article, doi)
                        resultFilenames.append(resultFilename)
                    break
            else:
                self.__logger.error("Could not find handler for "+ realLink)
            self.__logger.info("Doi reading finished")

        self.__logger.info("Finished analysing articles")
        return resultFilenames



