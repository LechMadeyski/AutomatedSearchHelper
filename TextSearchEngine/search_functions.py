from TextSearchEngine.merge_results import merge_results
from TextSearchEngine.find_in_text_json import find_in_text_json

import re


class EXACT_WORD:
    def __init__(self, word, case_sensitive=False):
        self._word = word
        self._case_sensitive = case_sensitive

    def __call__(self, data, finder_function=find_in_text_json):
        def matcherFunction(text):
            flags = 0
            if not self._case_sensitive:
                flags = re.IGNORECASE
            result = re.search(r'\b' + self._word + r'\b', text, flags)
            if result is not None:
                return (result.start(), result.end())
            else:
                return None

        return finder_function(data, matcherFunction)

    def __str__(self):
        return f'EXACT_WORD("{self._word}"{",case_sensitive" if self._case_sensitive else ""})'


class PARTIAL_WORD:
    def __init__(self, word, case_sensitive=False):
        self._word = word
        self._case_sensitive = case_sensitive

    def __call__(self, data, finder_function=find_in_text_json):
        def matcherFunction(text):
            flags = 0
            if not self._case_sensitive:
                flags = re.IGNORECASE
            result = re.search(self._word, text, flags)
            if result is not None:
                return (result.start(), result.end())
            else:
                return None

        return finder_function(data, matcherFunction)

    def __str__(self):
        return f'PARTIAL_WORD("{self._word}"{",case_sensitive" if self._case_sensitive else ""})'

class AND:
    def __init__(self, *matchers):
        self._matchers = matchers

    def __call__(self, data, finder_function=find_in_text_json, merge_function=merge_results):
        result = []
        for matcher in self._matchers:
            matchResult = matcher(data, finder_function)
            if matchResult is None:
                return None
            else:
                result.append(matchResult)
        return merge_function(result)

    def __str__(self):
        return f'AND({", ".join([str(matcher) for matcher in self._matchers])})'


class OR:
    def __init__(self, *matchers):
        self._matchers = matchers

    def __call__(self, data, finder_function=find_in_text_json, merge_function=merge_results):
        result = []
        for matcher in self._matchers:
            matchResult = matcher(data, finder_function)
            if matchResult is not None:
                result.append(matchResult)
        if len(result) > 0:
            return merge_function(result)
        else:
            return None

    def __str__(self):
        return f'OR({", ".join([str(matcher) for matcher in self._matchers])})'
