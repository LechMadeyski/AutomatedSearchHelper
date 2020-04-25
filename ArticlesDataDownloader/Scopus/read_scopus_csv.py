from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.csv_utilities import read_csv_as_dicts
from ArticlesDataDownloader.text_utilities import create_abstract

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
        doi=x.get('DOI', str())) for x in read_csv_as_dicts(filepath)]