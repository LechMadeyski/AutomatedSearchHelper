from bs4 import BeautifulSoup

import logging

from nltk import tokenize

def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


def springerHtmlToJson(textHTML):
    logging.info("Start readig Springer file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    logging.info("Reading section : Abstract" )
    abstractText = soup.findAll('section', {'class': 'Abstract'})[0].text

    abstractText = abstractText[len('Abstract'):]
    outputJson.append(
        {
        'title':'Abstract',
        'paragraphs' : [
            {
                "sentences" : formatTextAndSplitIntoSentences(abstractText)
            }
        ]})

    logging.debug("Abstract read correctly")

    for sec in soup.findAll('section', {"class": "Section1 RenderAsSection1"}):
        titles = sec.findAll('h2')
        title = ""
        if len(titles) > 0:
            title = titles[0].text
        else:
            title = ""
            logging.warining("Cannot find section title")

        paragraphs = []
        for par in sec.findAll('p'):
            paragraphs.append({"sentences": formatTextAndSplitIntoSentences(par.text)})

        logging.info("Reading section : "+ title )
        secData = {
            'title': title,
            'paragraphs' : paragraphs
        }
        outputJson.append(secData)

    return outputJson

