import re

from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.csv_utilities import read_csv_as_dicts
from ArticlesDataDownloader.text_utilities import create_abstract
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base


def __get_scopus_eid(article_dict):
    scopus_link = article_dict.get('Link', None)
    if scopus_link:
        document_id_search = re.findall("eid=(.*?)&", scopus_link)
        if document_id_search:
            return document_id_search[0]
    return str()


def __get_file_name_base(article_dict):
    doi = article_dict.get('DOI', str())
    if doi:
        return doi_to_filename_base(doi)
    document_id = __get_scopus_eid(article_dict)
    if document_id:
        return 'scopus_link_'+document_id
    return str()


def read_scopus_csv(filepath):
    return [ArticleData(
        authors=[author.strip() for author in x.get('Authors', str()).split(',')],
        scopus_link=x.get('Link', str()),
        title=x.get('Title', str()),
        publish_year=x.get('Year', str()),
        publisher=x.get('Publisher', str()),
        journal_name= x.get('Source title', str()),
        issue=x.get('Issue', str()),
        volume=x.get('Volume', str()),
        start_page=x.get('Page start', str()),
        end_page=x.get('Page end', str()),
        text=create_abstract(x.get('Abstract', str())),
        issn=x.get('ISSN', str()),
        publication_date=x.get('Conference date', str()),
        filename_base=__get_file_name_base(x),
        doi=x.get('DOI', str())) for x in read_csv_as_dicts(filepath)]