from .ArticleData import ArticleData
from crossref.restful import Works
import logging


class RefworksDataDownloader:
    def __init__(self):
        self.__works = Works()
        self.__logger = logging.getLogger("RefworksDataDownloader")

    def get_data(self, doi):
        data = ArticleData(doi=doi)
        try:
            doi_data = self.__works.doi(doi)
            data.publisher = doi_data.get("publisher", str())
            data.authors = [x.get('given', str()) + ' ' + x.get('family', str()) for x in
                                      doi_data.get("author", [])]
            data.title = ' '.join(doi_data.get("title", str()))
        except:
            self.__logger.error("some error while reading doi data")
            pass
        return data

