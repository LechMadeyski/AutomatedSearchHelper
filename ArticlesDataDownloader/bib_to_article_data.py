import bibtexparser

from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.text_utilities import create_abstract
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base
import re


def __start_page(entry):
    start_end_page = re.findall("[0-9]+", entry.get('pages', str()))
    if start_end_page:
        return start_end_page[0]
    return str()


def __end_page(entry):
    start_end_page = re.findall("[0-9]+", entry.get('pages', str()))
    if len(start_end_page) > 1:
        return start_end_page[1]
    return str()


def __doi(entry):
    return entry.get('doi', str())


def __publisher_link(entry):
    url = entry.get('url', None)
    if url and 'doi.org' not in url:
        return url
    else:
        return str()

def bib_text_to_article_datas_with_ids(text):
    fixed_text = '\n'.join([x for x in text.split('\n') if 'month = ' not in x])
    bib_database = bibtexparser.loads(fixed_text)
    return [(x.get('ID'), ArticleData(
        title=x.get('title', str()).replace('\n', ''),
        filename_base=doi_to_filename_base(x.get('doi', str())).replace('\n', ''),
        authors=x.get('author', str()).replace('\n', '').split(' and '),
        publish_year=x.get('year', str()).replace('\n', ''),
        issn=x.get('issn', str()).replace('\n', ''),
        publication_date=x.get('issue_date', str()).replace('\n', ''),
        publisher=x.get('publisher', str()).replace('\n', ''),
        journal_name=x.get('journal', str()) or x.get('booktitle', str()).replace('\n', ''),
        volume=x.get('volume', str()).replace('\n', ''),
        issue=x.get('number', str()).replace('\n', ''),
        start_page=__start_page(x),
        end_page=__end_page(x),
        publisher_link=__publisher_link(x),
        text=create_abstract(x.get('abstract', str())),
        doi=__doi(x))) for x in bib_database.entries]


def bib_text_to_article_data(text):
    datas = bib_text_to_article_datas_with_ids(text)
    if datas:
        return datas[0][1]
    else:
        return None


def bib_to_article_datas_with_ids(filepath):
    with open(filepath, encoding="utf-8") as bibtex_file:
        return bib_text_to_article_datas_with_ids(bibtex_file.read())
