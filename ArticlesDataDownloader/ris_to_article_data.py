
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.text_utilities import create_abstract

import rispy


def __entry_to_article_data(entry):
    return ArticleData(
        title=entry.get('title', str()) or entry.get('primary_title', str()),
        authors=entry.get('authors', list()),
        issn=entry.get('issn', str()),
        publisher=entry.get('publisher', str()),
        doi=entry.get('doi', str()).replace('https://doi.org/', str()),
        journal_name=entry.get('journal_name', str()),
        publish_year=entry.get('year', str()),
        publisher_link=entry.get('url', str()),
        volume=entry.get('volume', str()),
        issue=entry.get('number', str()),
        start_page=entry.get('start_page', str()),
        end_page=entry.get('end_page', str()),
        text=create_abstract(entry.get('abstract', str()) or entry.get('notes_abstract', str())))


def ris_text_to_article_data(text):
    entries = rispy.loads(text)
    for entry in entries:
        print('Analyzing entry ' + str(entry))
        return __entry_to_article_data(entry)
    raise AssertionError('Could not find proper ris entry')


def ris_to_article_data(filepath):
    with open(filepath, 'r', buffering=-1, encoding=None) as bibliography_file:
        return ris_text_to_article_data(bibliography_file.read())


def ris_to_article_datas(filepath):
    with open(filepath, 'r', buffering=-1, encoding=None) as bibliography_file:
        return [__entry_to_article_data(x) for x in rispy.loads(bibliography_file.read())]
