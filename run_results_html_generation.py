#!/usr/bin/env python

"""
Creates html representation of findings
"""

import argparse
import sys
import logging
import os
import json

from AutomatedSearchHelperUtilities.utilities import getDoiFilename, createDirectoryIfNotExistsOrClean
from SearchResultHtmlDisplay.findingsToHtml import findingsToHtml
import AutomatedSearchHelperUtilities.configuration as configuration


from distutils.dir_util import copy_tree


def run_results_html_generation(articles, outputFolder):
    createDirectoryIfNotExistsOrClean(outputFolder)

    staticIncludesPath = os.path.dirname(os.path.abspath(__file__)) + "/materialize"
    copy_tree(staticIncludesPath, outputFolder)

    logger = logging.getLogger("run_results_html_generation")
    for filename_base, articleData in articles.items():
        logger.info("Creating html for " + filename_base)
        with open(getDoiFilename(outputFolder, filename_base, "html"), 'w', encoding='utf-8') as f:
          f.write(findingsToHtml(articleData["article"], articleData["findings"]))


def prepareArticles(finderResultsFolder, articlesJsons):
    result = dict()

    for foundFilename in os.listdir(finderResultsFolder):
        articleFullPath = articlesJsons+"/"+foundFilename
        foundFullPath = finderResultsFolder + "/" + foundFilename
        with open(articleFullPath, 'r') as articleFile:
            with open(foundFullPath, 'r') as foundFile:
                foundData = json.load(foundFile)
                foundArticle = json.load(articleFile)
                result[foundArticle["filename_base"]] = {"article" : foundArticle, "findings" : foundData}
    return result

def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    parser.add_argument('--output_finder', default='outputFinder', type=str, help='Location for finder result .json files')
    parser.add_argument('--output_html', default='outputHtml', type=str, help='Location for result .html files')
    return parser


def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_results_html_generation')

    p = getArgumentsParser()
    a = p.parse_args(args=args)

    logger.info("Starting run_results_html_generation with following arguments")
    logger.info("output_articles = " + a.output_articles)
    logger.info("output_finder = " + str(a.output_finder))
    logger.info("output_html = " + a.output_html)

    run_results_html_generation(prepareArticles(a.output_finder, a.output_articles), a.output_html)


if __name__ == '__main__': sys.exit(main())