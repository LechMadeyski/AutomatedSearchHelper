from bs4 import BeautifulSoup

import logging

from nltk import tokenize

from ArticlesDataDownloader.format_text_and_split_into_sentences import format_text_and_split_into_sentences


def scienceDirectHtmlToJson(textHTML):
    logger = logging.getLogger("scienceDirectHtmlToJson")
    logger.info("Start readig ScienceDirect file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    logger.info("Reading section : Abstract" )
    abstractText = soup.findAll('div', {'class': 'Abstracts u-font-serif'})[0].text


    outputJson.append({
        'title':'Abstract',
        'paragraphs' : [{"sentences":format_text_and_split_into_sentences(abstractText)}]
    })

    logger.debug("Abstract read correctly")


    body = soup.find('div', {'id': 'body'})

    if not body:
        logger.error('Article has not body')
        raise ValueError("article has no body")

    for sec in body.findAll('section'):
        titles = sec.findAll('h2') + sec.findAll('h3')
        title = str()
        if len(titles) > 0:
            title = titles[0].text
        else:
            title = "unknown title"
            logger.warning("Found section with unknown title")

        paragraphs = []
        for par in sec.findAll('p'):
            paragraphs.append({"sentences": format_text_and_split_into_sentences(par.text)})

        logger.info("Reading section : " + title)
        sec_data = {
            'title': title,
            'paragraphs': paragraphs
        }
        outputJson.append(sec_data)
    return outputJson