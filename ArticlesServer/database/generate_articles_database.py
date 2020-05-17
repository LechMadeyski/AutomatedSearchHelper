import os

from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from TextSearchEngine.parse_finder import parse_finder
from .ArticlesDatabase import ArticlesDatabase
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
from ArticlesServer.directories import OUTPUT_DIRECTORY, OUTPUT_DB, PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES, \
    FINDER_FILE
import logging

from ArticlesDataDownloader.read_input_file import read_input_file

PROXY = 'proxy_auth_plugin.zip'

def __read_finder():
    if os.path.isfile(FINDER_FILE):
        with open(FINDER_FILE, 'r') as finder_file:
            return parse_finder(finder_file.read())

    def __none_finder():
        return None
    return __none_finder


def generate_articles_database_from_files():
    createDirectoryIfNotExists(OUTPUT_DIRECTORY)
    downloader = ArticlesDataDownloader(OUTPUT_DIRECTORY, PROXY)
    article_datas = []
    finder = __read_finder()

    logger = logging.getLogger('GenerateArticlesDatabase')

    for name, directory, input_type in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES:
        logger.info('Staring analysis of ' + name)
        for fileName in os.listdir(directory):
            logger.info('Analysing file: ' + fileName)
            search_datas = read_input_file(directory + '/' + fileName, input_type)
            no_or_articles = len(search_datas)
            logger.info('Analysing file: ' + fileName + ' articles to analyze ' + str(no_or_articles))
            for index, base_article_data in enumerate(search_datas):
                logger.info('Analyzing article ' + str(index+1) + '/' + str(no_or_articles))
                #logger.info('Article data ' + str(base_article_data))
                filename, article_data = downloader.read_article(base_article_data)
                if not article_data:
                    logger.error('Incorrect article data result')
                    continue
                search_result = finder(article_data.to_dict()) or {}

                duplicate = [x for x in article_datas if
                    x.get('base_article_data').filename_base and x.get('base_article_data').filename_base == base_article_data.filename_base
                    or (x.get('base_article_data').title and x.get('base_article_data').title == base_article_data.title
                        and x.get('base_article_data').authors == base_article_data.authors
                        and x.get('base_article_data').publisher == base_article_data.publisher)]
                if duplicate:
                    logger.info('Got duplicated article ' + str(base_article_data) + 'duplicate: ' + str(duplicate[0].get('base_article_data')))
                else:
                    article_datas.append(dict(article_data=article_data,
                                              findings=search_result,
                                              base_article_data=base_article_data))

    createDirectoryIfNotExists(OUTPUT_DB)
    return ArticlesDatabase(article_datas, OUTPUT_DB)
