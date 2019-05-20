from TextSearchEngine.mergeResults import mergeResults
from TextSearchEngine.findInTextJson import findInTextJson

import re

def EXACT_WORD(word, caseSensitive = False):
    def matcherFunction(text):
        flags = 0
        if not caseSensitive:
            flags = re.IGNORECASE
        result = re.search(r'\b'+ word + r'\b', text, flags)
        if result is not None:
            return (result.start(), result.end())
        else:
            return None
    def returnFunction(data, finderFunction = findInTextJson):
        return finderFunction(data, matcherFunction)
    return returnFunction

def PARTIAL_WORD(word, caseSensitive = False):
    def matcherFunction(text):
        flags = 0
        if not caseSensitive:
            flags = re.IGNORECASE
        result = re.search(word, text, flags)
        if result is not None:
            return (result.start(), result.end())
        else:
            return None
    def returnFunction(data, finderFunction = findInTextJson):
        return finderFunction(data, matcherFunction)
    return returnFunction


def AND(*textMatchers):
    def returnFunction(data, finderFunction = findInTextJson, mergeFunction = mergeResults):
        result = [];
        for matcher in textMatchers:
            matchResult = matcher(data, finderFunction)
            if matchResult is None:
                return None
            else:
                result.append(matchResult)
        return mergeFunction(result)

    return returnFunction


def OR(*textMatchers):
    def returnFunction(data, finderFunction = findInTextJson, mergeFunction = mergeResults):
        result = [];
        for matcher in textMatchers:
            matchResult = matcher(data, finderFunction)
            if matchResult is not None:
                result.append(matchResult)
        if len(result) > 0:
            return mergeFunction(result)
        else:
            return None

    return returnFunction
