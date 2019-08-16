import logging
import os
import json
import argparse
import configuration

from TextSearchEngine.search_functions import *
from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from doiList import doiList
from getDoiFilename import getDoiFilename
from SearchResultHtmlDisplay.findingsToHtml import findingsToHtml

from utilities import createDirectoryIfNotExists

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


def main():
    configuration.configureLogger()
    directoryForAritclesTexts = 'outputArticles'
    createDirectoryIfNotExists(directoryForAritclesTexts)

    downloader = ArticlesDataDownloader(directoryForAritclesTexts)

    directoryForFindResults = 'outputFinder'
    createDirectoryIfNotExists(directoryForFindResults)

    outputHtmlFolder = 'outputHtmls'
    createDirectoryIfNotExists(outputHtmlFolder)

    resultFiles = downloader.getDownloadArticles(doiList())

    finder = EXACT_WORD("C", case_sensitive= True)

    for filename in resultFiles:
      searchResult = None
      logging.info("Running finder for "+ filename)
      with open(filename, 'r') as f:
          articleText = json.load(f)
          searchResult = finder(articleText)

      if searchResult is not None:
        logging.info("Found something for doi "+ articleText["doi"] + ": " + str(searchResult))
        with open(getDoiFilename(directoryForFindResults, articleText["doi"]), 'w', encoding='utf-8') as f:
          f.write(json.dumps(searchResult))

        with open(getDoiFilename(outputHtmlFolder, articleText["doi"], "html"), 'w', encoding='utf-8') as f:
          f.write(findingsToHtml(articleText, searchResult))

        #logSearchResults(articleText, searchResult)


if __name__ == '__main__':
    main()