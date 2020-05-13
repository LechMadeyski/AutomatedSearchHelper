import bibtexparser

from ArticlesDataDownloader.ArticleData import ArticleData
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base


def __start_page(entry):
    start_end_page = entry.get('pages', str()).replace('\n', '').split('–')
    if start_end_page:
        return start_end_page[0]
    return str()


def __end_page(entry):
    start_end_page = entry.get('pages', str()).replace('\n', '').split('–')
    if len(start_end_page) > 1:
        return start_end_page[1]
    return str()


def bib_to_article_datas(filepath):
    with open(filepath) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        return [ArticleData(
            title=x.get('title', str()).replace('\n', ''),
            filename_base=doi_to_filename_base(x.get('doi', str())).replace('\n', ''),
            authors=x.get('author', str()).replace('\n', '').split(' and '),
            publish_year=x.get('year', str()).replace('\n', ''),
            issn=x.get('issn', str()).replace('\n', ''),
            publication_date=x.get('issue_date', str()).replace('\n', ''),
            publisher=x.get('publisher', str()).replace('\n', ''),
            journal_name=x.get('journal', str()) or x.get('booktitle', str()).replace('\n', ''),
            volume=x.get('volume', str()).replace('\n', ''),
            start_page=__start_page(x),
            end_page=__end_page(x),
            doi=x.get('doi', str())) for x in bib_database.entries]
