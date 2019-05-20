import pytest
from copy import deepcopy

from mergeResults import mergeResults

def test_mergeResultShouldReturnNoneIfEmptyResultsAreGiven():
    assert mergeResults([]) is None


def test_mergeResultShouldReturnSameResultIfOneIsGiven():
    exampleJson = [
        {
            "sectionIndex": 0,
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (2, 3)
                    ]
                }]
            }]
        }
    ]

    assert mergeResults([exampleJson]) == exampleJson



def test_properlyMergeDifferentSections():
    res1 = [
        {
            "sectionIndex": 2,
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (2, 3)
                    ]
                }]
            }]
        }
    ]


    res2 = [
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 1,
                "sentences" : [
                {
                    "sentenceIndex": 2,
                    "findings" :[
                        (3, 4)
                    ]
                }]
            }]
        },
        {
            "sectionIndex": 4,
            "paragraphs" : [
            {
                "paragraphIndex": 1,
                "sentences" : [
                {
                    "sentenceIndex": 2,
                    "findings" :[
                        (3, 4)
                    ]
                }]
            }]
        },
    ]


    expectedResult = [deepcopy(res2[0]), deepcopy(res1[0]), deepcopy(res2[1])]



    assert mergeResults([deepcopy(res1), deepcopy(res2)]) == expectedResult


def test_properlyMergeDifferentParagraphsInTheSameSection():
    res1 = [
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 3,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (1, 2)
                    ]
                }]
            }]
        }
    ]

    res2 = [
        {
            "sectionIndex": 0,
            "paragraphs" : [
            {
                "paragraphIndex": 1,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (1, 2)
                    ]
                }]
            },
            ]
        },
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 1,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (3, 4)
                    ]
                }]
            },
            {
                "paragraphIndex": 5,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (5, 6)
                    ]
                }]
            }
            ]
        }
    ]


    expectedResult = deepcopy(res2)
    expectedResult[1]["paragraphs"] = [ deepcopy(res2[1]["paragraphs"][0]), deepcopy(res1[0]["paragraphs"][0]),  deepcopy(res2[1]["paragraphs"][1])]

    assert mergeResults([res1, res2]) == expectedResult



def test_properlyMergeDifferentSentencesInTheSameParagraph():
    res1 = [
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 3,
                "sentences" : [
                {
                    "sentenceIndex": 3,
                    "findings" :[
                        (5, 6)
                    ]
                }]
            }]
        }
    ]

    res2 = [
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 0,
                "sentences" : [
                {
                    "sentenceIndex": 0,
                    "findings" :[
                        (7, 8)
                    ]
                }
                ]
            },
            {
                "paragraphIndex": 3,
                "sentences" : [
                {
                    "sentenceIndex": 1,
                    "findings" :[
                        (2, 5)
                    ]
                },
                {
                    "sentenceIndex": 5,
                    "findings" :[
                        (1, 5)
                    ]
                },

                ]
            }]
    }]

    expectedResult = deepcopy(res2)
    expectedResult[0]["paragraphs"][1]["sentences"] = [
                deepcopy(res2[0]["paragraphs"][1]["sentences"][0]),
                deepcopy(res1[0]["paragraphs"][0]["sentences"][0]),
                deepcopy(res2[0]["paragraphs"][1]["sentences"][1])]
    assert mergeResults([res1, res2]) == expectedResult



def test_properlyMergeFindingsInTheSameSentence():
    res1 = [
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 3,
                "sentences" : [
                {
                    "sentenceIndex": 3,
                    "findings" :[
                        (5, 7),
                        (10,20)
                    ]
                }]
            }]
        }
    ]

    res2 = [
        {
            "sectionIndex": 1,
            "paragraphs" : [
            {
                "paragraphIndex": 3,
                "sentences" : [
                {
                    "sentenceIndex": 1,
                    "findings" :[
                        (5, 6)
                    ]
                },
                {
                    "sentenceIndex": 3,
                    "findings" :[
                        (3, 5),
                        (7, 8)
                    ]
                }]
            }]
        }
    ]

    expectedResult = deepcopy(res2)
    expectedResult[0]["paragraphs"][0]["sentences"][1]["findings"] = [(3,8), (10,20)]
    assert mergeResults([res1, res2]) == expectedResult
