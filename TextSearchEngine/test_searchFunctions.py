import pytest

from TextSearchEngine.searchFunctions import OR, AND, EXACT_WORD, PARTIAL_WORD
from TextSearchEngine.mergeFindings import mergeFindings

def findFirstMatch(text, matcherFunction):
    return matcherFunction(text)

def test_EXACT_WORDShallFindExactWordInTestIfItsTheOnlyWord():
    sentence = "Aa"
    assert EXACT_WORD("Aa")(sentence, findFirstMatch) == (0,2)

def test_EXACT_WORDShallFindExactWordInTestIfItsInsideText():
    sentence = "Some Bb cc Aa Wda"
    assert EXACT_WORD("Aa")(sentence, findFirstMatch) == (11,13)

def test_EXACT_WORDShallNotFindExactWordInTestIfWordIsASubword():
    sentence = "Some Bb cc aAa WAda, Aaa, aAa"
    assert EXACT_WORD("Aa")(sentence, findFirstMatch) is None

def test_EXACT_WORDShallExactlyMatchIfCaseIsInsensitive():
    sentence = "aa"
    assert EXACT_WORD("Aa", caseSensitive = False)(sentence, findFirstMatch) == (0,2)

def test_EXACT_WORDShallNotFindMatchIfCaseIsSensitive():
    sentence = "aa"
    assert EXACT_WORD("Aa", caseSensitive = True)(sentence, findFirstMatch) == None

def test_EXACT_WORDShallFindExactWordInTestIfItsInsideTextOnlyCaseSensitive():
    sentence = "Some aa AA Aa aA"
    assert EXACT_WORD("Aa", caseSensitive = True)(sentence, findFirstMatch) == (11,13)

def test_PARTIAL_WORDCaseInsensitive():
    assert PARTIAL_WORD("Aa")("Aa", findFirstMatch) == (0,2)
    assert PARTIAL_WORD("Aa")("aa", findFirstMatch) == (0,2)
    assert PARTIAL_WORD("Aa")("aab", findFirstMatch) == (0,2)
    assert PARTIAL_WORD("Aa")("ddwAa", findFirstMatch) == (3,5)
    assert PARTIAL_WORD("Aa")("ddwAaWWE", findFirstMatch) == (3,5)
    assert PARTIAL_WORD("Aa")("addwWWWWEA", findFirstMatch) == None

def test_PARTIAL_WORDCaseSensitive():
    assert PARTIAL_WORD("Aa", caseSensitive = True)("Aa", findFirstMatch) == (0,2)
    assert PARTIAL_WORD("Aa", caseSensitive = True)("aa", findFirstMatch) == None
    assert PARTIAL_WORD("Aa", caseSensitive = True)("Aab", findFirstMatch) == (0,2)
    assert PARTIAL_WORD("Aa", caseSensitive = True)("ddwAa", findFirstMatch) == (3,5)
    assert PARTIAL_WORD("Aa", caseSensitive = True)("ddwAaWWE", findFirstMatch) == (3,5)
    assert PARTIAL_WORD("Aa", caseSensitive = True)("addwWWWWEA", findFirstMatch) == None

def test_ANDshallReturnResultIfOneResultIsOk():
    sentence = "Aa"
    assert AND(EXACT_WORD("Aa"))(sentence, findFirstMatch, mergeFindings) == [(0,2)]

def test_ANDshallReturnResultIfTwoResultsAreOk():
    sentence = "Aa, Cc Bb"
    assert AND(EXACT_WORD("Aa"), EXACT_WORD("bb"))(sentence, findFirstMatch, mergeFindings) == [(0,2), (7,9)]

def test_ANDshallReturnNoneIfOneResultYieldsNone():
    sentence = "Aa, Cc Bb"
    assert AND(EXACT_WORD("Aa"), EXACT_WORD("XX"), EXACT_WORD("bb"))(sentence, findFirstMatch, mergeFindings) == None

def test_ANDShallReturnNoneIfNoneIsMatching():
    sentence = "Aa, Cc Bb"
    assert AND(EXACT_WORD("WW"), EXACT_WORD("XX"), EXACT_WORD("SSs"))(sentence, findFirstMatch, mergeFindings) == None

def test_ORshallReturnResultIfOneResultIsOk():
    sentence = "Aa"
    assert OR(EXACT_WORD("Aa"))(sentence, findFirstMatch, mergeFindings) == [(0,2)]

def test_ORshallReturnResultIfTwoResultsAreOk():
    sentence = "Aa, Cc Bb"
    assert OR(EXACT_WORD("Aa"), EXACT_WORD("bb"))(sentence, findFirstMatch, mergeFindings) == [(0,2), (7,9)]

def test_ORshallReturnAllMatchingResultsEvenIfSomeAreNotOk():
    sentence = "Aa, Cc Bb"
    assert OR(EXACT_WORD("Aa"), EXACT_WORD("XX"), EXACT_WORD("bb"))(sentence, findFirstMatch, mergeFindings) == [(0,2), (7,9)]

def test_ORShallReturnNoneIfNoneIsMatching():
    sentence = "Aa, Cc Bb"
    assert OR(EXACT_WORD("WW"), EXACT_WORD("XX"), EXACT_WORD("SSs"))(sentence, findFirstMatch, mergeFindings) == None
