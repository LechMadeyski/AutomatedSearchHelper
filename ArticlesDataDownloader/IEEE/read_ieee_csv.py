from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.csv_utilities import read_csv_as_dicts
from ArticlesDataDownloader.text_utilities import create_abstract

import re

def get_publisher_link_from_pdf_link(pdf_link):
    if pdf_link:
        document_id = re.findall("arnumber=(.*?)/", pdf_link + '/')[0]
        return 'https://ieeexplore.ieee.org/document/' + document_id
    else:
        return str()

def read_ieee_csv(filepath):
    return [ArticleData(
        authors=[author.strip() for author in x.get('Authors', str()).split(';')],
        publisher_link=get_publisher_link_from_pdf_link(x.get('PDF Link')),
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
        doi=x.get('DOI', str())) for x in read_csv_as_dicts(filepath)]