import pytest

from .findInTextJson import findInTextJson


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
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (2, 3)]
                }]
            }]
        }
    ]

    assert findInTextJson(exampleJson, a_matcherFunction) == expectedResult

def test_shallFindWhenThereIsMultipleSentences():

    exampleJson = {
      "text": [
        {
          "paragraphs": [
            {
              "sentences": [
                "bba",
                "ccc",
                "bcaccca",
                "wqew",
                "",
                "a",
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
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (2, 3)]
                },
                {
                    "sentenceIndex": 2,
                    "findings" :[
                        (2, 3),
                        (6, 7)
                    ]
                },
                {
                    "sentenceIndex": 5,
                    "findings" :[
                        (0, 1)
                    ]
                }
                ]
            }]
        }
    ]

    assert findInTextJson(exampleJson, a_matcherFunction)[0]["paragraphs"][0]["sentences"] == expectedResult[0]["paragraphs"][0]["sentences"]

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
                "aaa",
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
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (2, 3),
                    ]
                }]
            },
            {
                "paragraphIndex": 2,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (0, 3)
                    ]
                }]
            },
            ]
        }
    ]

    assert findInTextJson(exampleJson, a_matcherFunction) == expectedResult


def test_shallFindInMultipleSections():
    exampleJson = {
      "text": [
        {
          "paragraphs": [
            {
              "sentences": [
                "ddd",
              ]
            },
            {
              "sentences": [
                "waa",
              ]
            }
          ],
          "title": "SomeTitle"
        },
        {
          "paragraphs": [
            {
              "sentences": [
                "www",
              ]
            },
          ],
          "title": "SomeTitle2"
        },
        {
          "paragraphs": [
            {
              "sentences": [
                "bb",
                "ca",
              ]
            },
          ],
          "title": "SomeTitle3"
        }


        ]
    }

    expectedResult = [
        {
            "sectionIndex": 0,
            "paragraphs" : [
            {
                "paragraphIndex": 1,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (1, 3),
                    ]
                }]
            },
            ]
        },
        {
            "sectionIndex": 2,
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 1,
                    "findings" :[
                        (1, 2),
                    ]
                },
                ]
            },
            ]
        }
    ]

    assert findInTextJson(exampleJson, a_matcherFunction) == expectedResult




