from ArticlesDataDownloader.ris_to_article_data import ris_to_article_datas


def read_science_direct_ris(filepath):
    return ris_to_article_datas(filepath)