import pytest
from .ArticlesDatabase import ArticlesDatabase


def generate_article_data(doi, title='some title', read_status = 'OK'):
    return dict(doi=doi, title=title, read_status=read_status)


def test_get_all_articles_shall_return_all_dois():
    articles_input = [
        {
            "article": generate_article_data('doidoi'),
            "findings": []
        },
        {
            "article": generate_article_data('doidoi2'),
            "findings": []
        }
    ]
    database = ArticlesDatabase(articles_input)
    assert database.get_all_articles_id() == ['doidoi', 'doidoi2']


def get_basic_articles():
    return [
        {
            "article": generate_article_data('d0', read_status='OK'),
            "findings": ['some finding', 'other finding']
        },
        {
            "article": generate_article_data('d1', read_status = 'OK'),
            "findings": []
        },
        {
            "article": generate_article_data('d2', read_status='Error....'),
            "findings": ['some finding']
        },
        {
            "article": generate_article_data('d3', read_status='OK'),
            "findings": ['some finding']
        },
        {
            "article": generate_article_data('d4', read_status='Other Error....'),
            "findings": ['some finding']
        },
        {
            "article": generate_article_data('d5', read_status='OK'),
            "findings": []
        },
    ]


def test_get_all_articles_of_given_type():
    database = ArticlesDatabase(get_basic_articles())
    assert database.get_all_valid_with_findings() == ['d0', 'd3']
    assert database.get_all_valid_without_findings() == ['d1', 'd5']
    assert database.get_all_invalid_articles() == ['d2', 'd4']

def test_get_next_article_shall_return_next_of_given_type():
    database = ArticlesDatabase(get_basic_articles())
    assert database.get_next_article('d0') == 'd3'
    assert database.get_next_article('d1') == 'd5'
    assert database.get_next_article('d2') == 'd4'
    assert database.get_next_article('d3') is None
    assert database.get_next_article('d5') is None
    assert database.get_next_article('d4') is None

def test_get_prev_article_shall_return_prev_of_given_type():
    database = ArticlesDatabase(get_basic_articles())
    assert database.get_prev_article('d3') == 'd0'
    assert database.get_prev_article('d4') == 'd2'
    assert database.get_prev_article('d5') == 'd1'
    assert database.get_prev_article('d0') is None
    assert database.get_prev_article('d1') is None
    assert database.get_prev_article('d2') is None

def test_get_full_article_shall_return_article():
    articles = get_basic_articles()
    database = ArticlesDatabase(articles)
    assert database.get_full_article('d0') == articles[0]
    assert database.get_full_article('d3') == articles[3]
