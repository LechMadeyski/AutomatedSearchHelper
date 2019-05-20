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
    def __init__(self, outputFolder):
        self.outputFolder = outputFolder
        self.__handlers = None

    def getDoiFilename(self, doi):
        return getDoiFilename(self.outputFolder, doi)

    def writeArticleToFile(self, article, doi):
        filename = self.getDoiFilename(doi)
        logging.info("Writing article to "+ filename)
        f = open(filename, "w")
        f.write(json.dumps({"text":article}))

    def doiHasResultAlready(self, doi):
        filename = self.getDoiFilename(doi)
        return os.path.isfile(filename)

    def getHandlers(self):
        if self.__handlers is None:
            driver = getDriver(use_proxy = True)
            self.__handlers = [
                IEEEArticlesHandler(driver),
                WilleyArticlesHandler(driver),
                ScienceDirectArticlesHandler(driver),
                ACMArticlesHandler(driver),
                SpringerArticlesHandler(driver),
            ]
        return self.__handlers

    def getDownloadArticles(self, doiList):
        logging.info("Start downloading articles")


        resultDoiAndFilename = []

        for doi in doiList:
            if self.doiHasResultAlready(doi):
                logging.info("Doi " + doi + " already parsed")
                resultDoiAndFilename.append({"doi":doi, "filename":self.getDoiFilename(doi)})
                continue

            logging.info("Reading doi : " + doi)
            realLink = getLinkFromDoi(doi)
            if doi is None:
                logging.error("Could not find link from doi")
                continue;
            logging.info ("Real link is " + realLink)

            for handler in self.getHandlers():
                logging.debug("Checking " + handler.name() + " with link part "+ handler.linkPart() )
                if handler.linkPart() in realLink:
                    logging.info("Link will be handled by " + handler.name())
                    article = handler.getArticle(realLink)

                    if article is None:
                        logging.error("Could not read article")
                    else:
                        resultFilename = self.writeArticleToFile(article, doi)
                        resultDoiAndFilename.append({"doi":doi, "filename":resultFilename})
                    break
            else:
                logging.error("Could not find handler for "+ realLink)
            logging.info("Doi reading finished")

        logging.info("Finished analysing articles")
        return resultDoiAndFilename



