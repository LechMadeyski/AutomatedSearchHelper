import pytest

from .search_functions import OR, AND, EXACT_WORD, PARTIAL_WORD
from .merge_findings import merge_findings


def find_first_match(text, matcherFunction):
    return matcherFunction(text)


def test_EXACT_WORDShallFindExactWordInTestIfItsTheOnlyWord():
    sentence = "Aa"
    assert EXACT_WORD("Aa")(sentence, find_first_match) == (0, 2)


def test_EXACT_WORDShallFindExactWordInTestIfItsInsideText():
    sentence = "Some Bb cc Aa Wda"
    assert EXACT_WORD("Aa")(sentence, find_first_match) == (11, 13)


def test_EXACT_WORDShallNotFindExactWordInTestIfWordIsASubword():
    sentence = "Some Bb cc aAa WAda, Aaa, aAa"
    assert EXACT_WORD("Aa")(sentence, find_first_match) is None


def test_EXACT_WORDShallExactlyMatchIfCaseIsInsensitive():
    sentence = "aa"
    assert EXACT_WORD("Aa", case_sensitive=False)(sentence, find_first_match) == (0, 2)


def test_EXACT_WORDShallNotFindMatchIfCaseIsSensitive():
    sentence = "aa"
    assert EXACT_WORD("Aa", case_sensitive=True)(sentence, find_first_match) == None


def test_EXACT_WORDShallFindExactWordInTestIfItsInsideTextOnlyCaseSensitive():
    sentence = "Some aa AA Aa aA"
    assert EXACT_WORD("Aa", case_sensitive=True)(sentence, find_first_match) == (11, 13)


def test_PARTIAL_WORDCaseInsensitive():
    assert PARTIAL_WORD("Aa")("Aa", find_first_match) == (0, 2)
    assert PARTIAL_WORD("Aa")("aa", find_first_match) == (0, 2)
    assert PARTIAL_WORD("Aa")("aab", find_first_match) == (0, 2)
    assert PARTIAL_WORD("Aa")("ddwAa", find_first_match) == (3, 5)
    assert PARTIAL_WORD("Aa")("ddwAaWWE", find_first_match) == (3, 5)
    assert PARTIAL_WORD("Aa")("addwWWWWEA", find_first_match) == None


def test_PARTIAL_WORDCaseSensitive():
    assert PARTIAL_WORD("Aa", case_sensitive=True)("Aa", find_first_match) == (0, 2)
    assert PARTIAL_WORD("Aa", case_sensitive=True)("aa", find_first_match) == None
    assert PARTIAL_WORD("Aa", case_sensitive=True)("Aab", find_first_match) == (0, 2)
    assert PARTIAL_WORD("Aa", case_sensitive=True)("ddwAa", find_first_match) == (3, 5)
    assert PARTIAL_WORD("Aa", case_sensitive=True)("ddwAaWWE", find_first_match) == (3, 5)
    assert PARTIAL_WORD("Aa", case_sensitive=True)("addwWWWWEA", find_first_match) == None


def test_ANDshallReturnResultIfOneResultIsOk():
    sentence = "Aa"
    assert AND(EXACT_WORD("Aa"))(sentence, find_first_match, merge_findings) == [(0, 2)]


def test_ANDshallReturnResultIfTwoResultsAreOk():
    sentence = "Aa, Cc Bb"
    assert AND(EXACT_WORD("Aa"), EXACT_WORD("bb"))(sentence, find_first_match, merge_findings) == [(0, 2), (7, 9)]


def test_ANDshallReturnNoneIfOneResultYieldsNone():
    sentence = "Aa, Cc Bb"
    assert AND(EXACT_WORD("Aa"), EXACT_WORD("XX"), EXACT_WORD("bb"))(sentence, find_first_match, merge_findings) == None


def test_ANDShallReturnNoneIfNoneIsMatching():
    sentence = "Aa, Cc Bb"
    assert AND(EXACT_WORD("WW"), EXACT_WORD("XX"), EXACT_WORD("SSs"))(sentence, find_first_match,
                                                                      merge_findings) == None


def test_ORshallReturnResultIfOneResultIsOk():
    sentence = "Aa"
    assert OR(EXACT_WORD("Aa"))(sentence, find_first_match, merge_findings) == [(0, 2)]


def test_ORshallReturnResultIfTwoResultsAreOk():
    sentence = "Aa, Cc Bb"
    assert OR(EXACT_WORD("Aa"), EXACT_WORD("bb"))(sentence, find_first_match, merge_findings) == [(0, 2), (7, 9)]


def test_ORshallReturnAllMatchingResultsEvenIfSomeAreNotOk():
    sentence = "Aa, Cc Bb"
    assert OR(EXACT_WORD("Aa"), EXACT_WORD("XX"), EXACT_WORD("bb"))(sentence, find_first_match, merge_findings) == [
        (0, 2), (7, 9)]


def test_ORShallReturnNoneIfNoneIsMatching():
    sentence = "Aa, Cc Bb"
    assert OR(EXACT_WORD("WW"), EXACT_WORD("XX"), EXACT_WORD("SSs"))(sentence, find_first_match, merge_findings) == None


def test_EXACT_WORD_shall_return_proper_to_string():
    finder = EXACT_WORD("AA", case_sensitive=False)
    assert str(finder) == 'EXACT_WORD("AA")'
    finder = EXACT_WORD("Ab cd ef", case_sensitive=True)
    assert str(finder) == 'EXACT_WORD("Ab cd ef",case_sensitive)'


def test_PARTIAL_WORD_shall_return_proper_to_string():
    finder = PARTIAL_WORD("AA", case_sensitive=False)
    assert str(finder) == 'PARTIAL_WORD("AA")'
    finder = PARTIAL_WORD("Ab cd ef", case_sensitive=True)
    assert str(finder) == 'PARTIAL_WORD("Ab cd ef",case_sensitive)'


def test_AND_shall_return_proper_to_string():
    finder = AND(EXACT_WORD("AA", case_sensitive=False))
    assert str(finder) == 'AND(EXACT_WORD("AA"))'

    finder = AND(EXACT_WORD("AA", case_sensitive=False), PARTIAL_WORD("AA", case_sensitive=True))
    assert str(finder) == 'AND(EXACT_WORD("AA"), PARTIAL_WORD("AA",case_sensitive))'

    finder = AND(EXACT_WORD("AA", case_sensitive=False),
                 AND(
                     PARTIAL_WORD("BB", case_sensitive=True),
                     EXACT_WORD("CC", case_sensitive=False)))
    assert str(finder) == 'AND(EXACT_WORD("AA"), ' \
                          'AND(PARTIAL_WORD("BB",case_sensitive), ' \
                          'EXACT_WORD("CC")))'


def test_OR_shall_return_proper_to_string():
    finder = OR(EXACT_WORD("AA", case_sensitive=False))
    assert str(finder) == 'OR(EXACT_WORD("AA"))'

    finder = OR(EXACT_WORD("AA", case_sensitive=False), PARTIAL_WORD("AA", case_sensitive=True))
    assert str(finder) == 'OR(EXACT_WORD("AA"), PARTIAL_WORD("AA",case_sensitive))'

    finder = OR(EXACT_WORD("AA", case_sensitive=False),
                 OR(
                     PARTIAL_WORD("BB", case_sensitive=True),
                     EXACT_WORD("CC", case_sensitive=False)))
    assert str(finder) == 'OR(EXACT_WORD("AA"), ' \
                          'OR(PARTIAL_WORD("BB",case_sensitive), ' \
                          'EXACT_WORD("CC")))'
