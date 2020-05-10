from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.csv_utilities import read_csv_as_dicts
from AutomatedSearchHelperUtilities.getDoiFilename import doi_to_filename_base


def __get_filename_base(article_dict):
    doi = article_dict.get('Item DOI', str())
    if doi:
        return doi_to_filename_base(doi)


def read_springer_csv(filepath):
    return [ArticleData(
        # Authors are incorrect in this file - not split into names
        title=x.get('Item Title', str()),
        publisher_link=x.get('URL', str()),
        publish_year=x.get('Publication Year', str()),
        journal_name= x.get('Publication Title', str()),
        filename_base=__get_filename_base(x),
        doi=x.get('Item DOI', str())) for x in read_csv_as_dicts(filepath) if x.get('Content Type', str()).strip() != 'Book']