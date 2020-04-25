from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.csv_utilities import read_csv_as_dicts
from ArticlesDataDownloader.text_utilities import create_abstract
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base

import re


def __get_document_id(article_dict):
    pdf_link = article_dict.get('PDF Link', None)
    if pdf_link:
        document_id_search = re.findall("arnumber=(.*?)/", pdf_link + '/')
        if document_id_search:
            return document_id_search[0]
    return str()


def __get_publisher_link(article_dict):
    document_id = __get_document_id(article_dict)
    if document_id:
        return 'https://ieeexplore.ieee.org/document/' + document_id
    else:
        return str()


def __get_file_name_base(article_dict):
    doi = article_dict.get('DOI', str())
    if doi:
        return doi_to_filename_base(doi)
    document_id = __get_document_id(article_dict)
    if document_id:
        return 'IEEE_'+document_id
    return str()


def read_ieee_csv(filepath):
    return [ArticleData(
        authors=[author.strip() for author in x.get('Authors', str()).split(';')],
        publisher_link=__get_publisher_link(x),
        title=x.get('Document Title', str()),
        publish_year=x.get('Publication Year', str()),
        publisher=x.get('Publisher', str()),
        journal_name= x.get('Publication Title', str()),
        issue=x.get('Issue', str()),
        volume=x.get('Volume', str()),
        start_page=x.get('Start Page', str()),
        end_page=x.get('End Page', str()),
        text=create_abstract(x.get('Abstract', str())),
        issn=x.get('ISSN', str()),
        doi=x.get('DOI', str()),
        filename_base=__get_file_name_base(x)
    ) for x in read_csv_as_dicts(filepath)]