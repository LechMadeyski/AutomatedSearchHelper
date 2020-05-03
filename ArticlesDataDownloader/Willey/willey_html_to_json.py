from bs4 import BeautifulSoup

import logging

from ArticlesDataDownloader.text_utilities import format_text_and_split_into_sentences


def willey_html_to_json(textHTML):
    logger = logging.getLogger("willeyHtmlToJson")
    logger.info("Start readig file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    for sec in soup.findAll(attrs={"class": "article-section__content"}):
        titles = sec.findAll('h2')
        title = ""
        if len(titles) > 0:
            title = titles[0].text
        else:
            title = "Abstract"  # first is always an abstract and has no text in h2(title)

        paragraphs = []
        for par in sec.findAll('p'):
            paragraphs.append({"sentences": format_text_and_split_into_sentences(par.text)})

        logger.info("Reading section : " + title)
        secData = {
            'title': title,
            'paragraphs': paragraphs
        }
        outputJson.append(secData)

    if len(outputJson) < 2:
        raise SyntaxError('Could not read full text')

    return outputJson
