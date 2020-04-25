#!/usr/bin/env python

"""
Runs finder in articles provided by user
"""

import argparse
import sys
import logging
import os
import json

from AutomatedSearchHelperUtilities.utilities import load_function, getDoiFilename, createDirectoryIfNotExistsOrClean
import AutomatedSearchHelperUtilities.configuration as configuration


def run_articles_search(articles, finder, outputDirectory=None):
    logger = logging.getLogger('run_articles_search')

    if outputDirectory is not None:
        createDirectoryIfNotExistsOrClean(outputDirectory)

    results = dict()
    for articleJsonFilename in articles:
        logger.info("reading file : "+ articleJsonFilename)
        searchResult = None
        with open(articleJsonFilename, 'r') as articleFile:
            articleData = json.load(articleFile)
            searchResult = finder(articleData)
        fileFoundStr = "some match found" if searchResult is not None else "nothing found"
        logger.info("File reading finished: " + fileFoundStr)

        if searchResult is not None:
            results[articleData["filename_base"]] = {"article" : articleData, "findings" : searchResult}
            if outputDirectory is not None:
                with open(getDoiFilename(outputDirectory, articleData["filename_base"]), 'w') as f:
                    f.write(json.dumps(searchResult))
    return results



def readArticles(articlesFolder):
    return [articlesFolder+"/"+f for f in os.listdir(articlesFolder) if f.endswith('.json')]

def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    parser.add_argument('--output_finder', default='outputFinder', type=str, help='Location for finder result .json files')
    parser.add_argument('--finder', default='finder.py', type=str, help='Python file containing global variable finder which is created using TextSearchEngine.searchFunctions')
    return parser


def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_articles_search')

    p = getArgumentsParser();
    a = p.parse_args(args=args)

    logger.info("Starting run_articles_search with following arguments")
    logger.info("output_articles = " + a.output_articles)
    logger.info("output_finder = " + str(a.output_finder))

    finder = load_function(a.finder, 'finder')

    logger.info("finder = " + str(a.finder))

    articles = readArticles(a.output_articles)

    logger.info("Following articles found in articles directory " + str(articles))

    run_articles_search(articles, finder, a.output_finder)



if __name__ == '__main__': sys.exit(main())