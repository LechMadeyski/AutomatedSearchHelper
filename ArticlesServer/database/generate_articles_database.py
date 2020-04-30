import os

from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from TextSearchEngine.parse_finder import parse_finder
from .ArticlesDatabase import ArticlesDatabase
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
from ArticlesServer.directories import OUTPUT_DIRECTORY, OUTPUT_DB, PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES, \
    FINDER_FILE

from ArticlesDataDownloader.read_input_file import read_input_file

PROXY = 'proxy_auth_plugin.zip'


def generate_articles_database(doi_list, finder):
    createDirectoryIfNotExists(OUTPUT_DIRECTORY)
    downloader = ArticlesDataDownloader(OUTPUT_DIRECTORY, PROXY)
    articlesData = []
    for doi in doi_list:
        articleFilename, data = downloader.readArticle(doi['doi'], doi['scopus_link'])
        searchResult = finder(data) or {}
        articlesData.append(dict(article=data, findings=searchResult))

    createDirectoryIfNotExists(OUTPUT_DB)
    return ArticlesDatabase(articlesData, OUTPUT_DB)


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
    for name, directory, input_type in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES:
        for fileName in os.listdir(directory):
            for base_article_data in read_input_file(directory + '/' + fileName, input_type):
                filename, article_data = downloader.read_article(base_article_data)
                search_result = finder(article_data) or {}
                if [x for x in article_datas if x.get('base_article_data').filename_base == base_article_data.filename_base]:
                    print('duplicated article found ' + base_article_data.filename_base)
                else:
                    article_datas.append(dict(article=article_data,
                                              findings=search_result,
                                              base_article_data=base_article_data))

    createDirectoryIfNotExists(OUTPUT_DB)
    return ArticlesDatabase(article_datas, OUTPUT_DB)
