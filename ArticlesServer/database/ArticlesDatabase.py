import operator
from collections import defaultdict

from .Status import Status


def try_to_find_next(article_id, doi_list):
    try:
        index = doi_list.index(article_id)
        if index < len(doi_list) - 1:
            return doi_list[index + 1]
    except ValueError:
        pass
    return None


def try_to_find_prev(article_id, doi_list):
    try:
        index = doi_list.index(article_id)
        if index > 0:
            return doi_list[index - 1]
    except ValueError:
        pass
    return None


class ArticlesDatabase:
    def __init__(self, files):
        self._articles = dict()
        self._valid_dois_with_findings = list()
        self._valid_dois_without_findings = list()
        self._invalid_dois = list()
        self._statuses = dict()
        self._comments = defaultdict(list)

        for index, file in enumerate(files):
            article_id = str(index)
            #            doi = file['article']['doi']
            self._articles[article_id] = file
            if file['article']['read_status'] == 'OK':
                if len(file['findings']) > 0:
                    self._valid_dois_with_findings.append(article_id)
                else:
                    self._valid_dois_without_findings.append(article_id)
            else:
                self._invalid_dois.append(article_id)
            self._statuses[article_id] = Status.TO_BE_CHECKED

    def get_full_article(self, article_id):
        return self._articles[article_id]

    def get_next_article(self, article_id):
        return try_to_find_next(article_id, self._valid_dois_with_findings) or \
               try_to_find_next(article_id, self._valid_dois_without_findings) or \
               try_to_find_next(article_id, self._invalid_dois)

    def get_prev_article(self, article_id):
        return try_to_find_prev(article_id, self._valid_dois_with_findings) or \
               try_to_find_prev(article_id, self._valid_dois_without_findings) or \
               try_to_find_prev(article_id, self._invalid_dois)

    def change_status(self, article_id, status):  # user??
        self._statuses[article_id] = status

    def get_status(self, article_id):  # user??
        return self._statuses[article_id]

    def get_all_articles_id(self):
        return list(self._articles.keys())

    def get_all_valid_with_findings(self):
        return self._valid_dois_with_findings

    def get_all_valid_without_findings(self):
        return self._valid_dois_without_findings

    def get_all_invalid_articles(self):
        return self._invalid_dois

    def get_short_article_info(self, article_id):
        article = self._articles[article_id]
        return {'id': article_id,
                'title': article['article']['title'],
                'doi': article['article']['doi'],
                'status': self.get_status(article_id)}

    def get_comments(self, article_id):
        return self._comments[article_id]

    def add_comment(self, article_id, comment, user):
        if len(self._comments[article_id]) > 0:
            comment_id = max(self._comments[article_id], key=lambda x: x['comment_id'])['comment_id']+1
        else:
            comment_id = 0
        self._comments[article_id].append(dict(comment_id=comment_id, text=comment, user=user))

    def remove_comment(self, article_id, comment_id):
        self._comments[article_id] = [x for x in self._comments[article_id] if x['comment_id'] != comment_id]

