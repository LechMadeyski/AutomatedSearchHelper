
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.text_utilities import create_abstract
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base

import rispy


def __entry_to_article_data(entry):
    result = ArticleData(
        title=entry.get('title', str()) or entry.get('primary_title', str()),
        authors=entry.get('authors', list()),
        issn=entry.get('issn', str()),
        publisher=entry.get('publisher', str()),
        doi=entry.get('doi', str()).replace('https://doi.org/', str()).replace('doi:', ''),
        journal_name=entry.get('journal_name', str()),
        publish_year=entry.get('year', str()),
        publisher_link=entry.get('url', str()),
        volume=entry.get('volume', str()),
        issue=entry.get('number', str()),
        start_page=entry.get('start_page', str()),
        end_page=entry.get('end_page', str()),
        publication_date=entry.get('date', str()) or entry.get('publication_year', str()),
        text=create_abstract(entry.get('abstract', str()) or entry.get('notes_abstract', str())))

    if 'doi.org' in result.publisher_link:
        result.publisher_link = str()

    if result.doi:
        result.filename_base = doi_to_filename_base(result.doi)
    return result


def ris_text_to_article_data(text):
    entries = rispy.loads(text)
    for entry in entries:
        return __entry_to_article_data(entry)
    raise AssertionError('Could not find proper ris entry')


def ris_to_article_data(filepath):
    with open(filepath, 'r', buffering=-1, encoding="utf-8") as bibliography_file:
        return ris_text_to_article_data(bibliography_file.read())


def ris_to_article_datas(filepath):
    with open(filepath, 'r', buffering=-1, encoding="utf-8") as bibliography_file:
        return [__entry_to_article_data(x) for x in rispy.loads(bibliography_file.read())]
