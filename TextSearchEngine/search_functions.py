from TextSearchEngine.merge_results import merge_results
from TextSearchEngine.find_in_text_json import find_in_text_json

import re


def EXACT_WORD(word, case_sensitive=False):
    def matcherFunction(text):
        flags = 0
        if not case_sensitive:
            flags = re.IGNORECASE
        result = re.search(r'\b' + word + r'\b', text, flags)
        if result is not None:
            return (result.start(), result.end())
        else:
            return None

    def returnFunction(data, finder_function=find_in_text_json):
        return finder_function(data, matcherFunction)

    return returnFunction


def PARTIAL_WORD(word, case_sensitive=False):
    def matcherFunction(text):
        flags = 0
        if not case_sensitive:
            flags = re.IGNORECASE
        result = re.search(word, text, flags)
        if result is not None:
            return (result.start(), result.end())
        else:
            return None

    def returnFunction(data, finder_function=find_in_text_json):
        return finder_function(data, matcherFunction)

    return returnFunction


def AND(*textMatchers):
    def returnFunction(data, finder_function=find_in_text_json, merge_function=merge_results):
        result = []
        for matcher in textMatchers:
            matchResult = matcher(data, finder_function)
            if matchResult is None:
                return None
            else:
                result.append(matchResult)
        return merge_function(result)

    return returnFunction


def OR(*textMatchers):
    def returnFunction(data, finder_function=find_in_text_json, merge_function=merge_results):
        result = []
        for matcher in textMatchers:
            matchResult = matcher(data, finder_function)
            if matchResult is not None:
                result.append(matchResult)
        if len(result) > 0:
            return merge_function(result)
        else:
            return None

    return returnFunction
