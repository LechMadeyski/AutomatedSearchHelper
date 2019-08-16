from bs4 import BeautifulSoup

import logging

from nltk import tokenize

def formatTextAndSplitIntoSentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


def scienceDirectHtmlToJson(textHTML):
    logger = logging.getLogger("scienceDirectHtmlToJson")
    logger.info("Start readig ScienceDirect file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    logger.info("Reading section : Abstract" )
    abstractText = soup.findAll('div', {'class': 'Abstracts u-font-serif'})[0].text


    outputJson.append({
        'title':'Abstract',
        'paragraphs' : [{"sentences":formatTextAndSplitIntoSentences(abstractText)}]
    })

    logger.debug("Abstract read correctly")

    generateSectionId = None
    if (soup.find(id="s0005")):
        def generateSecId(i):
            return "s"+str(10000 + i*5)[1:]
        generateSectionId = generateSecId
        logger.debug("Chosen sxxxx format")
    if (soup.find(id="sec0001")):
        def generateSecId(i):
            return "sec"+str(10000 + i)[1:]
        generateSectionId = generateSecId
        logger.debug("Chosen secxxxx format")

    if generateSectionId == None:
        logger.error("Could not find section id generator")
        return None



    for i in range(1,20):
        secId = generateSectionId(i)
        logger.info("looking for section " + secId)
        sec = soup.find(id = secId)
        if sec is None:
            break

        titles = sec.findAll('h2') + sec.findAll('h3')
        title = str()
        if len(titles) > 0:
            title = titles[0].text
        else:
            title = "unknown title"
            logger.warning("Found section with unknown title")

        paragraphs = []
        for par in sec.findAll('p'):
            paragraphs.append({"sentences" :formatTextAndSplitIntoSentences(par.text)})

        logger.info("Reading section : "+ title )
        sec_data = {
            'title': title,
            'paragraphs' : paragraphs
        }
        outputJson.append(sec_data)
    return outputJson

