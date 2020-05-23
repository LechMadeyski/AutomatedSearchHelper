from ArticlesDataDownloader.bib_to_article_data import bib_to_article_datas_with_ids


def read_willey_bib(filepath):
    return [x for _, x in bib_to_article_datas_with_ids(filepath)]