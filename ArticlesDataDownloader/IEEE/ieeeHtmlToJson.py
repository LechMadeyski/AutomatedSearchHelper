from bs4 import BeautifulSoup

import logging

from nltk import tokenize

def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


def ieeeHtmlToJson(textHTML):
    logging.info("Start readig IEEE file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    logging.info("Reading section : Abstract" )
    abstractText = soup.findAll('div', {'class': 'abstract-text row'})[0].text


    outputJson.append({
        'title':'Abstract',
        'paragraphs' : [{"sentences":formatTextAndSplitIntoSentences(abstractText)}]
    })

    logging.debug("Abstract read correctly")

    for sec in soup.findAll('div', {"class": "section"}):
        title = str(sec.findAll('h2')[0].text)

        paragraphs = [{"sentences": [title]}]
        for par in sec.findAll('p'):
            paragraphs.append({"sentences" :formatTextAndSplitIntoSentences(par.text)})

        logging.info("Reading section : "+ title )
        secData = {
            'title': title,
            'paragraphs' : paragraphs
        }
        outputJson.append(secData)

    return outputJson

