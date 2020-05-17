from ArticlesDataDownloader.bib_to_article_data import bib_to_article_datas_with_ids

def __correct_article_data_for_acm(data, bib_id):
    if not data.doi:
        data.doi = bib_id
    data.publisher_link = 'https://dl.acm.org/doi/'+data.doi
    return data

def read_acm_bib(filepath):
    return [__correct_article_data_for_acm(article_data, bib_id) for bib_id, article_data in bib_to_article_datas_with_ids(filepath)]