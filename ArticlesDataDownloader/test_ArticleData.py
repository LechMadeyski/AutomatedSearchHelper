import pytest
from .ArticleData import ArticleData
from copy import deepcopy


def test_merge_ArticleData_should_properly_merge_missing_data():
    emtpy_data = ArticleData()
    full_data = ArticleData(title="x",
                            doi='z',
                            publisher='w',
                            publisher_link= 'n',
                            scopus_link='e',
                            journal_info='q',
                            text=['something'],
                            authors=['quth'],
                            issn=['ewe'],
                            read_status='OK',
                            publish_year='1234',
                            journal_name='r')
    emtpy_data.merge(full_data)
    assert emtpy_data == full_data


def test_not_merge_if_already_filled():
    first_data = ArticleData(title="1",
                             doi='2',
                             publisher='3',
                             publisher_link='4',
                             scopus_link='5',
                             journal_info='6',
                             authors=['8'],
                             issn=['9'],
                             read_status='10',
                             publish_year='123',
                             journal_name='11')

    copied_first = deepcopy(first_data)

    full_data = ArticleData(title="x",
                            doi='z',
                            publisher='w',
                            publisher_link='n',
                            scopus_link='e',
                            journal_info='q',
                            authors=['quth'],
                            issn=['ewe'],
                            read_status='OK',
                            publish_year='555',
                            journal_name='r')
    first_data.merge(full_data)
    assert first_data == copied_first


def test_merge_ArticleData_should_properly_merge_all_missing_sections():
    first_data = ArticleData(text=[dict(
        title='Abstract',
        paragraphs=[dict(sentences='some some')]
    )])

    second_data = ArticleData(text=[
        dict(title='Any title2',
             paragraphs=[dict(sentences='anything')]),
        dict(title='Abstract',
             paragraphs=[dict(sentences='some some')]),
        dict(title='Any title',
             paragraphs=[dict(sentences='anything')])
    ])

    first_data.merge(second_data)

    assert first_data == ArticleData(text=[
        dict(title='Abstract',
             paragraphs=[dict(sentences='some some')]),
        dict(title='Any title2',
             paragraphs=[dict(sentences='anything')]),
        dict(title='Any title',
             paragraphs=[dict(sentences='anything')])
    ])
