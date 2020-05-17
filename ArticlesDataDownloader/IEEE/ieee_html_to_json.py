from bs4 import BeautifulSoup

import logging

from ArticlesDataDownloader.text_utilities import format_text_and_split_into_sentences


def ieee_html_to_json(textHTML):
    logger = logging.getLogger("ieeeHtmlToJson")
    logger.info("Start readig IEEE file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    logger.info("Reading section : Abstract" )
    abstractText = soup.findAll('div', {'class': 'abstract-text row'})[0].text


    outputJson.append({
        'title':'Abstract',
        'paragraphs' : [{"sentences":format_text_and_split_into_sentences(abstractText)}]
    })

    logger.debug("Abstract read correctly")

    for sec in soup.findAll('div', {"class": "section"}):
        title = str()
        titlesHtml = sec.findAll('h2')
        if len(titlesHtml) > 0:
            title = str(titlesHtml[0].text)

        paragraphs = [{"sentences": [title]}]
        for par in sec.findAll('p'):
            sentences = format_text_and_split_into_sentences(par.text)
            if len(sentences) > 0:
                paragraphs.append({"sentences" : sentences})

        logger.info("Reading section : "+ title )
        secData = {
            'title': title,
            'paragraphs' : paragraphs
        }
        outputJson.append(secData)

    if len(outputJson) < 3:
        raise Exception('Could not read pdf')

    return outputJson

