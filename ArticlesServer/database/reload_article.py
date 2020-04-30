from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from ArticlesServer.database.DatabaseManager import DatabaseManager
from ArticlesServer.directories import OUTPUT_DIRECTORY, FINDER_FILE
from TextSearchEngine.parse_finder import parse_finder
import os

PROXY = 'proxy_auth_plugin.zip'


def reload_article(article_id):
    print('Reloading article ' + article_id)
    db = DatabaseManager.get_instance()
    if not db:
        return
    article_data = db.get_full_article(article_id)

    print('Starting download')

    with open(FINDER_FILE, 'r') as finder_file:
        finder = parse_finder(finder_file.read())
    downloader = ArticlesDataDownloader(OUTPUT_DIRECTORY, PROXY)
    article_filename, data = downloader.read_article(article_data.search_base)
    if article_filename:
        os.remove(article_filename)
        article_filename, data = downloader.read_article(article_data.search_base)
    search_result = finder(data) or {}
    db.reload_article(article_id, data, search_result)