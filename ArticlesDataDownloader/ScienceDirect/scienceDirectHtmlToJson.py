from bs4 import BeautifulSoup

import logging

from nltk import tokenize

def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


def scienceDirectHtmlToJson(textHTML):
    logging.info("Start readig ScienceDirect file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    logging.info("Reading section : Abstract" )
    abstractText = soup.findAll('div', {'class': 'Abstracts u-font-serif'})[0].text


    outputJson.append({
        'title':'Abstract',
        'paragraphs' : [{"sentences":formatTextAndSplitIntoSentences(abstractText)}]
    })

    logging.debug("Abstract read correctly")

    for i in range(1,20):
        secId = "sec"+str(i)
        logging.info("looking for section " + secId)
        sec = soup.find(id = secId)
        if sec is None:
            break

        titles = sec.findAll('h2')
        title = ""
        if len(titles) > 0:
            title = titles[0].text
        else:
            title = "unknown title"
            logging.warning("Found section with unknown title")

        paragraphs = []
        for par in sec.findAll('p'):
            paragraphs.append({"sentences" :formatTextAndSplitIntoSentences(par.text)})

        logging.info("Reading section : "+ title )
        secData = {
            'title': title,
            'paragraphs' : paragraphs
        }
        outputJson.append(secData)
    return outputJson

