from ArticlesDataDownloader.ris_to_article_data import ris_to_article_datas

from ArticlesDataDownloader.ArticleData import ArticleData
import re


def __get_filename_base(publisher_link):
    if publisher_link:
        found_id = re.findall("/pii/(.*?)/", publisher_link + '/')
        if found_id:
            return 'science_direct_' + found_id[0]
    return str()


def read_science_direct_ris(filepath):
    res = ris_to_article_datas(filepath)
    [x.merge(ArticleData(publisher='Science Direct')) for x in res]
    [x.merge(ArticleData(filename_base=__get_filename_base(x.publisher_link))) for x in res if not x.filename_base]
    return res