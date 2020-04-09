from bs4 import BeautifulSoup

import logging

from ArticlesDataDownloader.format_text_and_split_into_sentences import format_text_and_split_into_sentences
from ArticlesDataDownloader.ArticleData import ArticleData


def get_abstract(soap):
    abstract_objects = soap.findAll('section', {'class': 'Abstract'})
    abstract_text = str()
    for abstract_obj in abstract_objects:
        for abstractPar in abstract_obj.findAll('p'):
            abstract_text += abstractPar.text
    if abstract_text:
        logging.debug("Abstract read correctly")
    else:
        logging.warning('Could not read abstract')
    return dict(title='Abstract', paragraphs=[dict(sentences=format_text_and_split_into_sentences(abstract_text))])


def get_full_text(soap):
    logging.info("Reading section : Abstract" )
    full_text = [get_abstract(soap)]
    for sec in soap.findAll('section', {"class": "Section1 RenderAsSection1"}):
        titles = sec.findAll('h2')
        title = titles[0].text if titles else str()
        logging.info("Reading section : <" + title + ">")
        paragraphs = list()
        for par in sec.findAll('p'):
            paragraphs.append({"sentences": format_text_and_split_into_sentences(par.text)})
        full_text.append(dict(title=title, paragraphs=paragraphs))
    return full_text


def springer_html_to_article_data(text_html):
    logging.info("Start reading Springer file")
    result = ArticleData()
    soap = BeautifulSoup(text_html, "html.parser")

    result.text = get_full_text(soap)
    return result

