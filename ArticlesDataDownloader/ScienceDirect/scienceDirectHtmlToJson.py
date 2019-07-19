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

    generateSectionId = None
    if (soup.find(id="s0005")):
        def generateSecId(i):
            return "s"+str(10000 + i*5)[1:]
        generateSectionId = generateSecId
        logging.debug("Chosen sxxxx format")
    if (soup.find(id="sec0001")):
        def generateSecId(i):
            return "sec"+str(10000 + i)[1:]
        generateSectionId = generateSecId
        logging.debug("Chosen secxxxx format")

    if generateSectionId == None:
        logging.error("Could not find section id generator")
        return None



    for i in range(1,20):
        secId = generateSectionId(i)
        logging.info("looking for section " + secId)
        sec = soup.find(id = secId)
        if sec is None:
            break

        titles = sec.findAll('h2') + sec.findAll('h3')
        title = str()
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

