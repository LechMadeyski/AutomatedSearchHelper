import pytest

from .parse_finder import parse_finder
from .search_functions import *


def test_parse_throw_when_opening_not_found():
    with pytest.raises(ValueError):
        parse_finder("")
    with pytest.raises(ValueError):
        parse_finder("EXACT_WORD_")


def test_parse_throw_when_unknown_method():
    with pytest.raises(ValueError):
        parse_finder("UNKNOWN()")


def test_parse_EXACT_WORD_shall_throw_when_word_is_not_found():
    with pytest.raises(ValueError):
        parse_finder('EXACT_WORD()')
    with pytest.raises(ValueError):
        parse_finder('EXACT_WORD(")')


def test_parse_EXACT_WORD_shall_throw_when_method_end_is_not_found():
    with pytest.raises(ValueError):
        parse_finder('EXACT_WORD("aAA"')


def test_parse_EXACT_WORD():
    text = 'EXACT_WORD("A")'
    finder = parse_finder(text)
    assert isinstance(finder, EXACT_WORD)
    assert str(finder) == 'EXACT_WORD("A")'


def test_parse_EXACT_WORD_with_case_sensitive():
    text = 'EXACT_WORD("A", case_sensitive)'
    finder = parse_finder(text)
    assert isinstance(finder, EXACT_WORD)
    assert str(finder) == 'EXACT_WORD("A",case_sensitive)'


def test_parse_PARTIAL_WORD():
    text = 'PARTIAL_WORD("A")'
    finder = parse_finder(text)
    assert isinstance(finder, PARTIAL_WORD)
    assert str(finder) == 'PARTIAL_WORD("A")'


def test_parse_PARTIAL_WORD_with_case_sensitive():
    text = 'PARTIAL_WORD("A", case_sensitive)'
    finder = parse_finder(text)
    assert isinstance(finder, PARTIAL_WORD)
    assert str(finder) == 'PARTIAL_WORD("A",case_sensitive)'


def test_parse_PARTIAL_WORD_ignore_spaces():
    text = ' PARTIAL_WORD ("A", case_sensitive ) '
    finder = parse_finder(text)
    assert isinstance(finder, PARTIAL_WORD)
    assert str(finder) == 'PARTIAL_WORD("A",case_sensitive)'


def test_parse_OR_single_matcher():
    text = 'OR(PARTIAL_WORD("A"))'
    finder = parse_finder(text)
    assert isinstance(finder, OR)
    assert str(finder) == 'OR(PARTIAL_WORD("A"))'


def test_parse_OR_two_simple_matchers():
    text = 'OR(PARTIAL_WORD("A"), EXACT_WORD("C"))'
    finder = parse_finder(text)
    assert isinstance(finder, OR)
    assert str(finder) == 'OR(PARTIAL_WORD("A"), EXACT_WORD("C"))'


def test_parse_OR_inside_OR():
    text = 'OR(PARTIAL_WORD("A"), OR(EXACT_WORD("B", case_sensitive), PARTIAL_WORD("D")))'
    finder = parse_finder(text)
    assert isinstance(finder, OR)
    assert str(finder) == 'OR(PARTIAL_WORD("A"), OR(EXACT_WORD("B",case_sensitive), PARTIAL_WORD("D")))'


def test_parse_AND_two_simple_matchers():
    text = 'AND(PARTIAL_WORD("A"), EXACT_WORD("C"))'
    finder = parse_finder(text)
    assert isinstance(finder, AND)
    assert str(finder) == 'AND(PARTIAL_WORD("A"), EXACT_WORD("C"))'


def test_parse_OR_AND_mix():
    text = 'OR(AND(PARTIAL_WORD("A"), EXACT_WORD("W")), AND(EXACT_WORD("B", case_sensitive), PARTIAL_WORD("D")))'
    finder = parse_finder(text)
    assert isinstance(finder, OR)
    assert str(finder) == 'OR(AND(PARTIAL_WORD("A"), EXACT_WORD("W")), AND(EXACT_WORD("B",case_sensitive), PARTIAL_WORD("D")))'
