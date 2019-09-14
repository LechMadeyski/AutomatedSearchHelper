from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from .ArticlesDatabase import ArticlesDatabase
from utilities import createDirectoryIfNotExists
from ArticlesServer.directories import OUTPUT_DIRECTORY, OUTPUT_DB

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
