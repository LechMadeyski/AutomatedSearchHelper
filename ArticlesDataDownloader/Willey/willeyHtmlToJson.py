from bs4 import BeautifulSoup

import logging

from nltk import tokenize


def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


def willeyHtmlToJson(textHTML):
    logger = logging.getLogger("willeyHtmlToJson")
    logger.info("Start readig file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    for sec in soup.findAll('div', {"class": "article-section__content"}):
        titles = sec.findAll('h2')
        title = ""
        if len(titles) > 0:
            title = titles[0].text
        else:
            title = "Abstract"  # first is always an abstract and has no text in h2(title)

        paragraphs = []
        for par in sec.findAll('p'):
            paragraphs.append({"sentences": formatTextAndSplitIntoSentences(par.text)})

        logger.info("Reading section : " + title)
        secData = {
            'title': title,
            'paragraphs': paragraphs
        }
        outputJson.append(secData)

    return outputJson
