import pytest



def findInTextJson(textJson, matcherFunction):
    result = []
    for sectionIndex in range(len(textJson["text"])):
        for paragraphIndex in range(len(textJson["text"][sectionIndex]["paragraphs"])):
            for sentenceIndex in range(len(textJson["text"][sectionIndex]["paragraphs"][paragraphIndex])):

                analyzedText = textJson["text"][sectionIndex]["paragraphs"][paragraphIndex]["sentences"][sentenceIndex]
                findResult = matcherFunction(analyzedText)
                while findResult is not None:
                    result.append(
                        {
                            "sectionIndex": sectionIndex,
                            "paragraphIndex": paragraphIndex,
                            "sentenceIndex": sentenceIndex,
                            "findPositionStart": findResult[0],
                            "findPositionEnd": findResult[1]
                        })
                    analyzedText = analyzedText[findResult[1]:]
                    findResult = matcherFunction(analyzedText)

    return result

def a_matcherFunction(text):
    pos = text.find("a")
    if pos == -1:
        return None
    return (pos, pos+1)


def test_shallFindWhenThereIsOneSentenceOnly():

    exampleJson = {
      "text": [
        {
          "paragraphs": [
            {
              "sentences": [
                "bba",
              ]
            }
          ],
          "title": "SomeTitle"
        }
        ]
    }

    expectedResult = [
        {
            "sectionIndex": 0,
            "paragraphIndex": 0,
            "sentenceIndex": 0,
            "findPositionStart": 2,
            "findPositionEnd": 3
        }
    ]

    assert findInTextJson(exampleJson, a_matcherFunction) == expectedResult

def test_shallFindInMultipleParagraphs():
    exampleJson = {
      "text": [
        {
          "paragraphs": [
            {
              "sentences": [
                "bba",
              ]
            },
            {
              "sentences": [
                "ddd",
              ]
            },
            {
              "sentences": [
                "aa",
              ]
            }
          ],
          "title": "SomeTitle"
        }
        ]
    }

    expectedResult = [
        {
            "sectionIndex": 0,
            "paragraphIndex": 0,
            "sentenceIndex": 0,
            "findPositionStart": 2,
            "findPositionEnd": 3
        },
        {
            "sectionIndex": 0,
            "paragraphIndex": 2,
            "sentenceIndex": 0,
            "findPositionStart": 0,
            "findPositionEnd": 1
        },
        {
            "sectionIndex": 0,
            "paragraphIndex": 2,
            "sentenceIndex": 0,
            "findPositionStart": 0,
            "findPositionEnd": 1
        }
    ]

    assert findInTextJson(exampleJson, a_matcherFunction) == expectedResult



