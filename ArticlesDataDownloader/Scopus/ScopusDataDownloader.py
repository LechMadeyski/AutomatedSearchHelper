from bs4 import BeautifulSoup
from nltk import tokenize
from selenium.webdriver.support.wait import WebDriverWait
import logging
from ArticlesDataDownloader.ArticleData import ArticleData

def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


PUBLISHER = 'Publisher: '
ISSN = 'ISSN: '
DOI = 'DOI: '

def prepare_default(scopus_link):
    return ArticleData(scopus_link = scopus_link)

class ScopusDataDownloader:

    def __init__(self, driver):
        self._driver = driver
        self._logger = logging.getLogger('ScopusDataDownloader')

    def _try_getting_data(self, link):
        self._logger.info('Trying to read ' + link)
        self._logger.info("Calling get")
        self._driver.get(link)

        WebDriverWait(self._driver, 10).until(
            lambda x: self._driver.find_element_by_xpath("//section[@id='abstractSection']"))

        result = prepare_default(link)
        self._logger.info("Got link preparin soap")
        soup = BeautifulSoup(self._driver.page_source, "html.parser")
        self._logger.info("Got soap - analysis start")
        abstract_text = soup.findAll('section', {'id': 'abstractSection'})[0].findAll('p')[0].text
        result.text = [
            {'title': 'Abstract', 'paragraphs': [{'sentences': formatTextAndSplitIntoSentences(abstract_text)}]}]
        journal_name = soup.findAll('span', {'id': "publicationTitle"})
        if journal_name:
            result.journal_name = journal_name[0].text
        else:
            result.journal_name = soup.findAll('span', {'id': "noSourceTitleLink"})[0].text
        result.journal_info = soup.findAll('span', {'id': "journalInfo"})[0].text
        result.title = soup.find('h2', {'class': "h3"}).findAll(text=True, recursive=False)[0].strip()
        authors_base = soup.findAll('section', {'id': 'authorlist'})
        if authors_base:
            authors_html = authors_base[0].findAll('li')
            result.authors = []
            for item in authors_html:
                author = item.findAll('span', {'class': "anchorText"})
                if len(author) > 0:
                    result.authors.append(author[0].text)

        for ref in soup.findAll('section', {'id': 'referenceInfo'})[0].findAll('li'):
            pub_idx = ref.text.find(PUBLISHER)
            if pub_idx != -1:
                result.publisher = ref.text[pub_idx + len(PUBLISHER):]

            issn_idx = ref.text.find(ISSN)
            if issn_idx != -1:
                result.issn = ref.text[issn_idx + len(ISSN):].strip()
            doi_idx = ref.text.find(DOI)
            if doi_idx != -1:
                result.doi = ref.text[doi_idx+len(DOI):].strip()

        self._logger.info("Soap analysis end")
        return result

    def get_data(self, link):
        if link and link != str():
            return self._try_getting_data(link)

        self._logger.error('Could not read data from ' + link)
        return prepare_default(link)
