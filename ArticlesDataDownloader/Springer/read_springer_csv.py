from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.csv_utilities import read_csv_as_dicts


def read_springer_csv(filepath):
    return [ArticleData(
        # Authors are incorrect in this file - not split into names
        title=x.get('Item Title', str()),
        publisher_link=x.get('URL', str()),
        publish_year=x.get('Publication Year', str()),
        journal_name= x.get('Publication Title', str()),
        doi=x.get('Item DOI', str())) for x in read_csv_as_dicts(filepath)]