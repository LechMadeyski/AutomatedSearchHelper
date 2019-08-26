import pytest

from .Status import Status
from .ArticlesDatabase import ArticlesDatabase


def generate_article_data(doi, title='some title', read_status='OK'):
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
    assert database.get_all_articles_id() == ['0', '1']


def get_basic_articles():
    return [
        {
            "article": generate_article_data('d0', read_status='OK'),
            "findings": ['some finding', 'other finding']
        },
        {
            "article": generate_article_data('d1', read_status='OK'),
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
    ids = database.get_all_articles_id()
    assert database.get_all_valid_with_findings() == [ids[0], ids[3]]
    assert database.get_all_valid_without_findings() == [ids[1], ids[5]]
    assert database.get_all_invalid_articles() == [ids[2], ids[4]]


def test_get_next_article_shall_return_next_of_given_type():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()

    assert database.get_next_article(ids[0]) == ids[3]
    assert database.get_next_article(ids[1]) == ids[5]
    assert database.get_next_article(ids[2]) == ids[4]
    assert database.get_next_article(ids[3]) is None
    assert database.get_next_article(ids[4]) is None
    assert database.get_next_article(ids[5]) is None


def test_get_prev_article_shall_return_prev_of_given_type():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()

    assert database.get_prev_article(ids[3]) == ids[0]
    assert database.get_prev_article(ids[4]) == ids[2]
    assert database.get_prev_article(ids[5]) == ids[1]
    assert database.get_prev_article(ids[0]) is None
    assert database.get_prev_article(ids[1]) is None
    assert database.get_prev_article(ids[2]) is None


def test_get_full_article_shall_return_article():
    articles = get_basic_articles()
    database = ArticlesDatabase(articles)
    ids = database.get_all_articles_id()

    assert database.get_full_article(ids[0]) == articles[0]
    assert database.get_full_article(ids[3]) == articles[3]


def test_get_status_shall_return_to_be_checked_by_default():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()

    assert database.get_status(ids[0]) == Status.TO_BE_CHECKED
    assert database.get_status(ids[3]) == Status.TO_BE_CHECKED


def test_change_status_shall_properly_set_status():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()

    database.change_status(ids[0], Status.ACCEPTED)
    database.change_status(ids[1], Status.TO_BE_CHECKED)
    database.change_status(ids[4], Status.DECLINED)

    assert database.get_status(ids[0]) == Status.ACCEPTED
    assert database.get_status(ids[1]) == Status.TO_BE_CHECKED
    assert database.get_status(ids[3]) == Status.TO_BE_CHECKED
    assert database.get_status(ids[4]) == Status.DECLINED


def test_comments_shall_be_empty_for_basic():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()
    assert database.get_comments(ids[0]) == list()
    assert database.get_comments(ids[4]) == list()


def test_adding_comments():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()

    database.add_comment(ids[0], "a", user="U1")
    assert database.get_comments(ids[0]) == [dict(comment_id=0, text="a", user="U1")]
    assert database.get_comments(ids[4]) == list()

    database.add_comment(ids[1], "b b", user="U2")
    assert database.get_comments(ids[1]) == [dict(comment_id=0, text="b b", user="U2")]

    database.add_comment(ids[0], "c", user="U2")
    assert database.get_comments(ids[0]) == [dict(comment_id=0, text="a", user="U1"),
                                             dict(comment_id=1, text="c", user="U2")]

    database.add_comment(ids[0], "e", user="U1")
    assert database.get_comments(ids[0]) == [dict(comment_id=0, text="a", user="U1"),
                                             dict(comment_id=1, text="c", user="U2"),
                                             dict(comment_id=2, text="e", user="U1")]


def test_removing_comments():
    database = ArticlesDatabase(get_basic_articles())
    ids = database.get_all_articles_id()

    database.add_comment(ids[0], "a", user="U1")
    database.add_comment(ids[0], "c", user="U1")
    database.add_comment(ids[0], "e", user="U1")
    assert database.get_comments(ids[0]) == [dict(comment_id=0, text="a", user="U1"),
                                             dict(comment_id=1, text="c", user="U1"),
                                             dict(comment_id=2, text="e", user="U1")]
    database.remove_comment(ids[0], 0)
    assert database.get_comments(ids[0]) == [dict(comment_id=1, text="c", user="U1"),
                                             dict(comment_id=2, text="e", user="U1")]

    database.remove_comment(ids[0], 2)
    assert database.get_comments(ids[0]) == [dict(comment_id=1, text="c", user="U1")]

    database.remove_comment(ids[0], 2)
    assert database.get_comments(ids[0]) == [dict(comment_id=1, text="c", user="U1")]
    database.remove_comment(ids[0], 0)

    database.add_comment(ids[0], "w", user="U1")
    assert database.get_comments(ids[0]) == [dict(comment_id=1, text="c", user="U1"),
                                             dict(comment_id=2, text="w", user="U1")]
