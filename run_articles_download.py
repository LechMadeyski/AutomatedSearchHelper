#!/usr/bin/env python

"""
Downloads articles from input, to given folder in .json format
"""

import argparse
import sys
import logging
from AutomatedSearchHelperUtilities.extract_doi_from_csv import extract_doi_from_csv
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
import AutomatedSearchHelperUtilities.configuration as configuration
from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader

def run_articles_download(outputArticles, doiList, proxyFile):
    createDirectoryIfNotExists(outputArticles)
    downloader = ArticlesDataDownloader(outputArticles, proxyFile)
    return downloader.getDownloadArticles(doiList)

def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    parser.add_argument('--doi_list', default='dois.csv', type=str, help='CSV file containing DOI column with DOIs of articles')
    parser.add_argument('--proxy_file', default='proxy_auth_plugin.zip', type=str, help='Proxy configuration file')
    return parser


def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_articles_download')

    p = getArgumentsParser()
    a = p.parse_args(args=args)

    logger.info("Starting run_articles_download with following arguments")
    logger.info("output_articles = " + a.output_articles)

    doi_list = extract_doi_from_csv(a.doi_list)
    logger.info("doi_list = " + str(doi_list))

    run_articles_download(a.output_articles, doi_list, a.proxy_file)


if __name__ == '__main__': sys.exit(main())
