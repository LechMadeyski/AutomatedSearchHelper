import os

from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from TextSearchEngine.parse_finder import parse_finder
from .ArticlesDatabase import ArticlesDatabase
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
from ArticlesServer.directories import OUTPUT_DIRECTORY, OUTPUT_DB, PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES, \
    FINDER_FILE
import logging
import random

from ArticlesDataDownloader.read_input_file import read_input_file

PROXY = 'proxy_auth_plugin.zip'

def __read_finder():
    if os.path.isfile(FINDER_FILE):
        with open(FINDER_FILE, 'r') as finder_file:
            return parse_finder(finder_file.read())

    def __none_finder(arg):
        return None
    return __none_finder


def get_duplicates(all_datas, given_data):
    return [x for x in all_datas if
                 x.get('base_article_data').filename_base and x.get(
                     'base_article_data').filename_base == given_data.filename_base
                 or (x.get('base_article_data').title and x.get('base_article_data').title == given_data.title
                     and x.get('base_article_data').authors == given_data.authors
                     and x.get('base_article_data').publisher == given_data.publisher)]

def append_or_inform_about_duplicate(all_datas, base_data, given_data, finder):
    duplicates = get_duplicates(all_datas, given_data)
    if duplicates:
        logger = logging.getLogger('GenerateArticlesDatabase')
        logger.info('Got duplicated article ' + str(given_data.filename_base) + 'duplicate: '
                    + str(duplicates[0].get('base_article_data').filename_base))
        logger.debug('Got duplicated article ' + str(given_data) + 'duplicate: '
                     + str(duplicates[0].get('base_article_data')))
    else:
        search_result = finder(given_data.to_dict()) or {}
        all_datas.append(dict(article_data=given_data,
                              findings=search_result,
                              base_article_data=base_data))


def generate_articles_database_from_files():
    createDirectoryIfNotExists(OUTPUT_DIRECTORY)
    createDirectoryIfNotExists(OUTPUT_DB)
    downloader = ArticlesDataDownloader(OUTPUT_DIRECTORY, PROXY)
    article_datas = []
    article_datas_to_be_downloaded = []

    finder = __read_finder()

    logger = logging.getLogger('GenerateArticlesDatabase')

    for name, directory, input_type in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES:
        logger.info('Staring analysis of ' + name)
        for fileName in os.listdir(directory):
            logger.info('Analysing file: ' + fileName)
            search_datas = read_input_file(os.path.join(directory, fileName), input_type)
            no_or_articles = len(search_datas)
            logger.info('Analysing file: ' + fileName + ' articles to analyze ' + str(no_or_articles))
            for index, base_article_data in enumerate(search_datas):
                logger.debug('Analyzing article ' + str(index+1) + '/' + str(no_or_articles))
                filename, article_data = downloader.load_archived_article_data(base_article_data)
                if filename and article_data:
                    append_or_inform_about_duplicate(article_datas, base_article_data, article_data, finder)
                elif not get_duplicates(article_datas, base_article_data):
                    article_datas_to_be_downloaded.append(base_article_data)

    logger.info('Successfully reloaded ' + str(len(article_datas)) + ' articles')

    if article_datas_to_be_downloaded:
        random.shuffle(article_datas_to_be_downloaded) # to prevent ip blocks
        no_of_articles_to_be_reloaded = str(len(article_datas_to_be_downloaded))
        logger.info('Got ' + no_of_articles_to_be_reloaded + ' articles to download')

        for index, base_article_data in enumerate(article_datas_to_be_downloaded):
            logger.info('Downloading article ' + str(index+1) + '/' + no_of_articles_to_be_reloaded + ' : ' + base_article_data.filename_base)
            filename, article_data = downloader.read_article(base_article_data)
            if not article_data:
                logger.error('Incorrect article data result')
                continue
            append_or_inform_about_duplicate(article_datas, base_article_data, article_data, finder)

    article_datas.sort(key=lambda x: x['article_data'].filename_base)



    return ArticlesDatabase(article_datas, OUTPUT_DB)
