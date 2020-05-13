from ArticlesDataDownloader.bib_to_article_data import bib_to_article_datas


def read_acm_bib(filepath):
    return bib_to_article_datas(filepath)