import bibtexparser

from ArticlesDataDownloader.ArticleData import ArticleData
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base


def __start_page(entry):
    start_end_page = entry.get('pages', str()).split('–')
    if start_end_page:
        return start_end_page[0]
    return str()


def __end_page(entry):
    start_end_page = entry.get('pages', str()).split('–')
    if len(start_end_page) > 1:
        return start_end_page[1]
    return str()


def bib_to_article_datas(filepath):
    with open(filepath) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        return [ArticleData(
            title=x.get('title', str()),
            filename_base=doi_to_filename_base(x.get('doi', str())),
            authors=x.get('author', str()).split(' and '),
            publish_year=x.get('year', str()),
            issn=x.get('issn', str()),
            publication_date=x.get('issue_date', str()),
            publisher=x.get('publisher', str()),
            journal_name=x.get('journal', str()) or x.get('booktitle', str()),
            volume=x.get('volume', str()),
            start_page=__start_page(x),
            end_page=__end_page(x),
            doi=x.get('doi', str())) for x in bib_database.entries]
