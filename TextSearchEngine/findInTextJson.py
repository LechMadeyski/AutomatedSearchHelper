from TextSearchEngine.mergeFindings import mergeFindings

def findInSentece(sentenceText, matcherFunction):
    findings = []
    findResult = matcherFunction(sentenceText)
    offset = 0
    while findResult is not None:
        findings.append((offset + findResult[0], offset + findResult[1]))
        offset += findResult[1]
        sentenceText = sentenceText[findResult[1]:]
        findResult = matcherFunction(sentenceText)
    findings = mergeFindings(findings)
    return findings

def findInParagraph(paragraphText, matcherFunction):
    sentencesFindings = []
    for sentenceIndex in range(len(paragraphText["sentences"])):
        sentenceResult = {
                "sentenceIndex" : sentenceIndex,
                "findings" : findInSentece(paragraphText["sentences"][sentenceIndex], matcherFunction)
            }
        if len(sentenceResult["findings"]) > 0:
            sentencesFindings.append(sentenceResult)
    return sentencesFindings

def findInSection(sectionText, matcherFunction):
    sectionFindings = []
    for paragraphIndex in range(len(sectionText["paragraphs"])):
        paragraphResult = {
                "paragraphIndex" : paragraphIndex,
                "sentences": findInParagraph(sectionText["paragraphs"][paragraphIndex], matcherFunction)
            }
        if len(paragraphResult["sentences"]) > 0:
            sectionFindings.append(paragraphResult)
    return sectionFindings

def findInTextJson(textJson, matcherFunction):
    result = []
    for sectionIndex in range(len(textJson["text"])):
        sectionResult = {
            "sectionIndex" : sectionIndex,
            "paragraphs" : findInSection(textJson["text"][sectionIndex], matcherFunction)}
        if len(sectionResult["paragraphs"]) > 0:
            result.append(sectionResult)


    if len(result) < 1:
        return None

    return result
