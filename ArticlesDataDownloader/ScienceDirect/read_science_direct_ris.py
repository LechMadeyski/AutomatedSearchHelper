from ArticlesDataDownloader.ris_to_article_data import ris_to_article_datas

from ArticlesDataDownloader.ArticleData import ArticleData

def read_science_direct_ris(filepath):
    res = ris_to_article_datas(filepath)
    [x.merge(ArticleData(publisher='Science Direct')) for x in res]
    return res