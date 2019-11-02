from bs4 import BeautifulSoup
from nltk import tokenize
import time
import logging

def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


PUBLISHER = 'Publisher: '
ISSN = 'ISSN: '
DOI = 'DOI: '
def prepare_default():
    return {
        'text': list(),
        'journalName': str(),
        'journalInfo': str(),
        'title': str(),
        'authors': list(),
        'publisher': str(),
        'issn':str(),
        'scopus_link':str()
    }

class ScopusDataDownloader:

    def __init__(self, driver):
        self._driver = driver
        self._logger = logging.getLogger('ScopusDataDownloader')

    def _try_getting_data(self, link):
        self._logger.info('Trying to read ' + link)
        self._driver.get(link)
        result = prepare_default()
        result['scopus_link'] = link
        soup = BeautifulSoup(self._driver.page_source, "html.parser")
        abstract_text = soup.findAll('section', {'id': 'abstractSection'})[0].findAll('p')[0].text
        result['text'] = [
            {'title': 'Abstract', 'paragraphs': [{'sentences': formatTextAndSplitIntoSentences(abstract_text)}]}]
        journalName = soup.findAll('span', {'id': "publicationTitle"})
        if journalName:
            result['journalName'] = journalName[0].text
        else:
            result['journalName'] = soup.findAll('span', {'id': "noSourceTitleLink"})[0].text
        result['journalInfo'] = soup.findAll('span', {'id': "journalInfo"})[0].text
        result['title'] = soup.find('h2', {'class': "h3"}).findAll(text=True, recursive=False)[0].strip()
        authors_base = soup.findAll('section', {'id': 'authorlist'})
        if authors_base:
            authors_html = authors_base[0].findAll('li')
            result['authors'] = []
            for item in authors_html:
                author = item.findAll('span', {'class': "anchorText"})
                if len(author) > 0:
                    result['authors'].append(author[0].text)

        for ref in soup.findAll('section', {'id': 'referenceInfo'})[0].findAll('li'):
            pub_idx = ref.text.find(PUBLISHER)
            if pub_idx != -1:
                result['publisher'] = ref.text[pub_idx + len(PUBLISHER):]

            issn_idx = ref.text.find(ISSN)
            if issn_idx != -1:
                result['issn'] = ref.text[issn_idx + len(ISSN):]
            doi_idx = ref.text.find(DOI)
            if doi_idx != -1:
                result['doi'] = ref.text[doi_idx+len(DOI):]
        return result

    def get_data(self, link):
        if link:
            for i in range(3):
                try:
                    return self._try_getting_data(link)
                except:
                    time.sleep(2)
            return self._try_getting_data(link)

        self._logger.error('Could not read data from ' + link)
        return prepare_default()
