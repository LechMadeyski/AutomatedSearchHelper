import pytest
from ArticlesDataDownloader.ArticleData import ArticleData

from .Status import Status
from .ArticlesDatabase import ArticlesDatabase


def generate_article_data(doi, title='some title', read_status='OK'):
    return ArticleData(doi=doi, title=title, read_status=read_status)


def test_get_all_articles_shall_return_all_dois():
    articles_input = [
        {
            "article_data": generate_article_data('doidoi'),
            "findings": []
        },
        {
            "article_data": generate_article_data('doidoi2'),
            "findings": []
        }
    ]
    database = ArticlesDatabase(articles_input, "someTestPath")
    assert database.get_all_articles_id() == ['0', '1']


def get_basic_articles():
    return [
        {
            "article_data": generate_article_data('d0', read_status='OK'),
            "findings": ['some finding', 'other finding']
        },
        {
            "article_data": generate_article_data('d1', read_status='OK'),
            "findings": []
        },
        {
            "article_data": generate_article_data('d2', read_status='Error....'),
            "findings": ['some finding']
        },
        {
            "article_data": generate_article_data('d3', read_status='OK'),
            "findings": ['some finding']
        },
        {
            "article_data": generate_article_data('d4', read_status='Other Error....'),
            "findings": ['some finding']
        },
        {
            "article_data": generate_article_data('d5', read_status='OK'),
            "findings": []
        },
    ]



def test_get_full_article_shall_return_article():
    articles = get_basic_articles()
    database = ArticlesDatabase(articles, "someTestPath")
    ids = database.get_all_articles_id()

    assert database.get_full_article(ids[0]).findings == articles[0]['findings']
    assert database.get_full_article(ids[3]).findings == articles[3]['findings']


def test_get_status_shall_return_to_be_checked_by_default():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
    ids = database.get_all_articles_id()

    assert database.get_status(ids[0], 'user1') == Status.TO_BE_CHECKED
    assert database.get_status(ids[3], 'user1') == Status.TO_BE_CHECKED


def test_change_status_shall_properly_set_status():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
    ids = database.get_all_articles_id()

    user = 'user'

    database.change_status(ids[0], user, Status.ACCEPTED)
    database.change_status(ids[1], user, Status.TO_BE_CHECKED)
    database.change_status(ids[4], user, Status.DECLINED)

    assert database.get_status(ids[0], user) == Status.ACCEPTED
    assert database.get_status(ids[1], user) == Status.TO_BE_CHECKED
    assert database.get_status(ids[3], user) == Status.TO_BE_CHECKED
    assert database.get_status(ids[4], user) == Status.DECLINED


def test_change_status_shall_properly_set_status_for_proper_user():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
    ids = database.get_all_articles_id()

    user1 = 'user1'
    user2 = 'user2'

    assert database.get_status(ids[0], user1) == Status.TO_BE_CHECKED
    assert database.get_status(ids[0], user2) == Status.TO_BE_CHECKED

    database.change_status(ids[0], user1, Status.ACCEPTED)
    database.change_status(ids[0], user2, Status.DECLINED)

    assert database.get_status(ids[0], user1) == Status.ACCEPTED
    assert database.get_status(ids[0], user2) == Status.DECLINED

def test_get_statuses_without_user_shall_return_statuses_in_user_order():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
    ids = database.get_all_articles_id()

    user1 = 'user1'
    user2 = 'user2'
    user3 = 'user3'

    database.change_status(ids[0], user1, Status.ACCEPTED)
    database.change_status(ids[0], user2, Status.DECLINED)
    database.change_status(ids[0], user3, Status.TO_BE_CHECKED)

    assert database.get_statuses(ids[0]) == [(user1, Status.ACCEPTED),
                                             (user2, Status.DECLINED),
                                             (user3, Status.TO_BE_CHECKED)]


def test_get_statuses_without_user_shall_return_statuses_including_user_and_with_given_user_first():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
    ids = database.get_all_articles_id()

    user1 = 'user1'
    user2 = 'user2'
    user3 = 'user3'
    user4 = 'user4'

    database.change_status(ids[0], user1, Status.ACCEPTED)
    database.change_status(ids[0], user2, Status.DECLINED)
    database.change_status(ids[0], user3, Status.TO_BE_CHECKED)

    assert database.get_statuses(ids[0], user1) == [(user1, Status.ACCEPTED),
                                             (user2, Status.DECLINED),
                                             (user3, Status.TO_BE_CHECKED)]

    assert database.get_statuses(ids[0], user2) == [(user2, Status.DECLINED),
                                             (user1, Status.ACCEPTED),
                                             (user3, Status.TO_BE_CHECKED)]

    assert database.get_statuses(ids[0], user4) == [(user4, Status.TO_BE_CHECKED),
                                             (user1, Status.ACCEPTED),
                                             (user2, Status.DECLINED),
                                             (user3, Status.TO_BE_CHECKED)]


def test_comments_shall_be_empty_for_basic():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
    ids = database.get_all_articles_id()
    assert database.get_comments(ids[0]) == list()
    assert database.get_comments(ids[4]) == list()


def test_adding_comments():
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
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
    database = ArticlesDatabase(get_basic_articles(), "someTestPath")
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
