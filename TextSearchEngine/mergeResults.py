from copy import deepcopy
from TextSearchEngine.mergeFindings import mergeFindings
def takeSectionIndex(elem):
    return elem["sectionIndex"]

def takeParagraphIndex(elem):
    return elem["paragraphIndex"]

def takeSentenceIndex(elem):
    return elem["sentenceIndex"]

def mergeSentences(finalResultSentence, sentenceToBeMerged):
    finalResultSentence["findings"] = mergeFindings(finalResultSentence["findings"] + sentenceToBeMerged["findings"])

def mergeParagraphs(finalResultParagraph, paragraphToBeMerged):
    for sentenceToBeMerged in paragraphToBeMerged["sentences"]:
        matchingSentence = [x for x in finalResultParagraph["sentences"] if sentenceToBeMerged["sentenceIndex"] == x["sentenceIndex"]]
        if len(matchingSentence) < 1:
            finalResultParagraph["sentences"].append(deepcopy(sentenceToBeMerged))
        else:
            mergeSentences(matchingSentence[0], sentenceToBeMerged)
    finalResultParagraph["sentences"].sort(key=takeSentenceIndex)


def mergeSections(finalResultSection, sectionToBeMerged):
    for paragraphToBeMerged in sectionToBeMerged["paragraphs"]:
        matchingParagraph = [x for x in finalResultSection["paragraphs"] if paragraphToBeMerged["paragraphIndex"] == x["paragraphIndex"]]
        if len(matchingParagraph) < 1:
            finalResultSection["paragraphs"].append(deepcopy(paragraphToBeMerged))
        else:
            mergeParagraphs(matchingParagraph[0], paragraphToBeMerged)
    finalResultSection["paragraphs"].sort(key=takeParagraphIndex)

def mergeResults(items):
    finalResult = None
    for item in items:
        if finalResult is None:
            finalResult = deepcopy(item)
            continue
        for sectionToBeMerged in item:
            matchingSection = [x for x in finalResult if sectionToBeMerged["sectionIndex"] == x["sectionIndex"]]
            if len(matchingSection) < 1:
                finalResult.append(deepcopy(sectionToBeMerged))
            else:
                mergeSections(matchingSection[0], sectionToBeMerged)
        finalResult.sort(key=takeSectionIndex)
    return finalResult