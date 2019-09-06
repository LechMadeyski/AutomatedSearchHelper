from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from .ArticlesDatabase import ArticlesDatabase
from utilities import createDirectoryIfNotExists

OUTPUT_DIRECTORY = 'outputArticles'
PROXY = 'proxy_auth_plugin.zip'
OUTPUT_DB = 'outputComments'

def generate_articles_database(doi_list, finder):
    downloader = ArticlesDataDownloader(OUTPUT_DIRECTORY, PROXY)
    articlesData = []
    for doi in doi_list:
        articleFilename, data = downloader.readArticle(doi['doi'], doi['scopus_link'])
        searchResult = finder(data) or {}
        articlesData.append(dict(article=data, findings=searchResult))

    createDirectoryIfNotExists(OUTPUT_DB)
    return ArticlesDatabase(articlesData, OUTPUT_DB)
