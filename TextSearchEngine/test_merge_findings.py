import pytest

from .merge_findings import merge_findings

def test_mergeFindingsShallReturnEmptyRangeIfEmptyWasGiven():
    assert merge_findings([]) == []

def test_mergeFindingsShallReturnSameRangeIfOneWasGiven():
    assert merge_findings([(1, 6)]) == [(1, 6)]


def test_mergeFindingsShallReturnSeparateRangesIfAllWereSeparateWasGiven():
    assert merge_findings([(1, 6), (8, 11), (12, 13)]) == [(1, 6), (8, 11), (12, 13)]

def test_mergeFindingsShallProperlyMergeTwoRanges():
    assert merge_findings([(1, 6), (6, 7)]) == [(1, 7)]

def test_mergeFindingsShallProperlyMergeTwoOverlappingRanges():
    assert merge_findings([(1, 6), (3, 7)]) == [(1, 7)]

def test_mergeFindingsShallProperlyMergeThreeOverlappingRanges():
    assert merge_findings([(1, 6), (3, 5), (2, 7)]) == [(1, 7)]

def test_mergeFindingsShallProperlyMergeTwoSeparateSetsOfRanges():
    assert merge_findings([(1, 6), (3, 7), (71, 78), (75, 87)]) == [(1, 7), (71, 87)]
