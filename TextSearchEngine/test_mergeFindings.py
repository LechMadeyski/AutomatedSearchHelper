import pytest

from TextSearchEngine.mergeFindings import mergeFindings

def test_mergeFindingsShallReturnEmptyRangeIfEmptyWasGiven():
    assert mergeFindings([]) == []

def test_mergeFindingsShallReturnSameRangeIfOneWasGiven():
    assert mergeFindings([(1,6)]) == [(1,6)]


def test_mergeFindingsShallReturnSeparateRangesIfAllWereSeparateWasGiven():
    assert mergeFindings([(1,6), (8,11), (12,13)]) == [(1,6), (8,11), (12,13)]

def test_mergeFindingsShallProperlyMergeTwoRanges():
    assert mergeFindings([(1,6), (6,7)]) == [(1,7)]

def test_mergeFindingsShallProperlyMergeTwoOverlappingRanges():
    assert mergeFindings([(1,6), (3,7)]) == [(1,7)]

def test_mergeFindingsShallProperlyMergeThreeOverlappingRanges():
    assert mergeFindings([(1,6), (3, 5), (2,7)]) == [(1,7)]

def test_mergeFindingsShallProperlyMergeTwoSeparateSetsOfRanges():
    assert mergeFindings([(1,6), (3, 7), (71,78), (75,87)]) == [(1,7), (71,87)]
