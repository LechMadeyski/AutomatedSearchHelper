from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from .ArticlesDatabase import ArticlesDatabase

OUTPUT_DIRECTORY = 'outputArticles'
PROXY = 'proxy_auth_plugin.zip'


def generate_articles_database(doi_list, finder):
    downloader = ArticlesDataDownloader(OUTPUT_DIRECTORY, PROXY)

    articlesData = []
    for doi in doi_list:
        articleFilename, data = downloader.readArticle(doi)
        searchResult = finder(data) or {}
        articlesData.append(dict(article=data, findings=searchResult))

    return ArticlesDatabase(articlesData)
