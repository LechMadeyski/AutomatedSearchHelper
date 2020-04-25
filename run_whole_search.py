#!/usr/bin/env python

"""
Downloads articles from input, to given folder in .json format
Then runs finder for it and creates html output
"""

import argparse
import sys
import logging

from ArticlesDataDownloader.read_input_file import read_input_file
from AutomatedSearchHelperUtilities.utilities import load_variable

from run_articles_download import run_articles_download
from run_articles_search import run_articles_search
from run_results_html_generation import run_results_html_generation
from AutomatedSearchHelperUtilities.extract_doi_from_csv import extract_doi_from_csv
import AutomatedSearchHelperUtilities.configuration as configuration

def run_whole_search(article_datas, finder, output_articles, output_finder, output_html, proxy_file):

    logger = logging.getLogger('run_whole_search')

    logger.info("Articles download start")
    articlesDownloadResult = run_articles_download(output_articles, article_datas, proxy_file)

    logger.info("Articles searching start")

    searchResult = run_articles_search(articlesDownloadResult, finder, output_finder)

    logger.info("Html generation start")

    if output_html != None:
        run_results_html_generation(searchResult, output_html)



def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    parser.add_argument('--output_finder', default='outputFinder', type=str, help='Location for finder result .json files')
    parser.add_argument('--output_html', default='outputHtml', type=str, help='Location for result .html files')
    parser.add_argument('--finder', default='finder.py', type=str, help='Python file containing global variable finder which is created using TextSearchEngine.searchFunctions')
    parser.add_argument('--proxy_file', default='proxy_auth_plugin.zip', type=str, help='Proxy configuration file')
    parser.add_argument('--articles_list', type=str, help='file containing articles data in supported format')
    parser.add_argument('--file_type', default=1, type=int, help='File format: '
                                                                 '1- SCOPUS_CSV (default), '
                                                                 '2- IEEE_CSV '
                                                                 '3- SCIENCE_DIRECT_RIS, '
                                                                 '4- SPRINGER_CSV'
                                                                 '5- WILLEY_RIS'
                                                                 '6- ACM_BIB')
    return parser


def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_whole_search')

    p = getArgumentsParser()
    a = p.parse_args(args=args)

    logger.info("Starting run_whole_search with following arguments")
    logger.info("output_articles = " + a.output_articles)
    logger.info("output_finder = " + str(a.output_finder))
    logger.info("output_html = " + a.output_html)

    article_datas = read_input_file(a.articles_list, a.file_type)

    finder = load_variable(a.finder, 'finder')

    logger.info("finder = " + str(a.finder))
    logger.info("doi_list = " + str(article_datas))

    run_whole_search(article_datas, finder, a.output_articles, a.output_finder, a.output_html, a.proxy_file)


if __name__ == '__main__': sys.exit(main())