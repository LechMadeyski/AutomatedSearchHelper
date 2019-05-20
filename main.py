import logging
import os
import json
from TextSearchEngine.searchFunctions import *
from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from doiList import doiList
from getDoiFilename import getDoiFilename
from SearchResultHtmlDisplay.findingsToHtml import findingsToHtml

def configureLogger():
    logsFilename = 'AutomatedSearchHelper.log'
    with open(logsFilename, 'w'):
        pass
    logging.basicConfig(filename=logsFilename, format='%(asctime)s %(levelname)s/%(message)s', level=logging.INFO)
    logging.info("Starting new run")


def logSearchResults(articleText, searchResult):
  for resultSection in searchResult:
      logging.info("Something found in section "+ articleText["text"][resultSection["sectionIndex"]]["title"] )
      for paragraph in resultSection["paragraphs"]:
          parIndex = paragraph["paragraphIndex"]
          for sentence in paragraph["sentences"]:
            sentIndex = sentence["sentenceIndex"]
            fullSentence = articleText["text"][resultSection["sectionIndex"]]["paragraphs"][parIndex]["sentences"][sentIndex]

            for finding in reversed(sentence["findings"]):
              fullSentence = fullSentence[:finding[0]] + "!!!<" + fullSentence[finding[0]:finding[1]] + ">!!!"+ fullSentence[finding[1]:]
            logging.info(fullSentence)

def createDirectoryIfNotExists(folderName):
  if not os.path.exists(folderName):
      logging.info("Creating directory " + folderName)
      os.makedirs(folderName)

def main():
    configureLogger()
    directoryForAritclesTexts = 'outputArticles'
    createDirectoryIfNotExists(directoryForAritclesTexts)

    downloader = ArticlesDataDownloader(directoryForAritclesTexts)

    directoryForFindResults = 'outputFinder'
    createDirectoryIfNotExists(directoryForFindResults)

    outputHtmlFolder = 'outputHtmls'
    createDirectoryIfNotExists(outputHtmlFolder)

    resultFiles = downloader.getDownloadArticles(doiList())

    finder = EXACT_WORD("C", caseSensitive = True)

    for doiAndFilename in resultFiles:
      searchResult = None
      logging.info("Running finder for "+ doiAndFilename["doi"])
      with open(doiAndFilename["filename"], 'r') as f:
          articleText = json.load(f)
          searchResult = finder(articleText)

      if searchResult is not None:
        logging.info("Found something for doi "+ doiAndFilename["doi"] + ": " + str(searchResult))
        with open(getDoiFilename(directoryForFindResults, doiAndFilename["doi"]), 'w', encoding='utf-8') as f:
          f.write(json.dumps(searchResult))

        with open(getDoiFilename(outputHtmlFolder, doiAndFilename["doi"], "html"), 'w', encoding='utf-8') as f:
          f.write(findingsToHtml(articleText, searchResult))

        #logSearchResults(articleText, searchResult)


if __name__ == '__main__':
    main()