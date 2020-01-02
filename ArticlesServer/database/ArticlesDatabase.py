from collections import defaultdict

from .ArticleData import ArticleData
from .Status import Status
import json

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
    def __init__(self, files, output_db):
        self._articles = dict()
        self._valid_dois_with_findings = list()
        self._valid_dois_without_findings = list()
        self._invalid_dois = list()
        self._statuses = defaultdict(dict)
        self._comments = defaultdict(list)
        self._output_db = output_db
        for index, file in enumerate(files):
            article_id = str(index)
            self._articles[article_id] = ArticleData(file)
            article_data = self._articles[article_id]
            print('reading article no: ' + article_id + ' name: '  + article_data.doi)
            self._assign_to_category(article_data, article_id)

        self._load_comments_and_statuses()

    def _assign_to_category(self, article_data, article_id):
        if article_data.findings:
            self._valid_dois_with_findings.append(article_id)
        elif article_data.read_status == 'OK':
            self._valid_dois_without_findings.append(article_id)
        else:
            self._invalid_dois.append(article_id)

    def _load_comments_and_statuses(self):
        for article_id in self._articles.keys():
            file_path = self._create_comments_filename(article_id)
            try:
                with open(file_path, 'r') as file_object:
                    self._comments[article_id] = json.load(file_object)
            except FileNotFoundError:
                pass

            file_path = self._create_statuses_filename(article_id)
            try:
                with open(file_path, 'r') as file_object:
                    self._statuses[article_id] = json.load(file_object)
                    for user in self._statuses[article_id].keys():
                        self._statuses[article_id][user] = Status(self._statuses[article_id][user])
            except FileNotFoundError:
                pass

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

    def change_status(self, article_id, user, status):
        self._statuses[article_id][user] = status
        self._update_statuses(article_id)

    def get_status(self, article_id, user):
        return self._statuses[article_id].get(user, Status.TO_BE_CHECKED)

    def get_statuses(self, article_id, login = None):
        if not login:
            return [(key, value) for key, value in self._statuses[article_id].items()]

        ret = [(key, value) for key, value in self._statuses[article_id].items() if key != login]
        ret = [(login, self.get_status(article_id, login))] + ret
        return ret

    def get_all_articles_id(self):
        return list(self._articles.keys())

    def get_all_valid_with_findings(self):
        return self._valid_dois_with_findings

    def get_all_valid_without_findings(self):
        return self._valid_dois_without_findings

    def get_all_invalid_articles(self):
        return self._invalid_dois

    def get_short_article_info(self, article_id, user = None):
        article_data = self._articles[article_id]
        return {'id': article_id,
                'title': article_data.title,
                'doi': article_data.doi,
                'statuses': self.get_statuses(article_id, user)}

    def get_comments(self, article_id):
        return self._comments[article_id]

    def add_comment(self, article_id, comment, user):
        if len(self._comments[article_id]) > 0:
            comment_id = max(self._comments[article_id], key=lambda x: x['comment_id'])['comment_id']+1
        else:
            comment_id = 0
        self._comments[article_id].append(dict(comment_id=comment_id, text=comment, user=user))
        self._update_comments(article_id)

    def remove_comment(self, article_id, comment_id):
        self._comments[article_id] = [x for x in self._comments[article_id] if x['comment_id'] != comment_id]
        self._update_comments(article_id)

    def _create_comments_filename(self, article_id):
        return self._output_db + \
               "/" + self._articles[article_id].doi.replace('/', '_') + "_comments.json"

    def _create_statuses_filename(self, article_id):
        return self._output_db + \
               "/" + self._articles[article_id].doi.replace('/', '_') + "_status.json"

    def _update_comments(self, article_id):
        file_path = self._create_comments_filename(article_id)
        try:
            with open(file_path, 'w') as file_object:
                json.dump(self._comments[article_id], file_object)
        except FileNotFoundError:
            print(file_path + " not found. ")

    def _update_statuses(self, article_id):
        file_path = self._create_statuses_filename(article_id)
        try:
            with open(file_path, 'w') as file_object:
                json.dump(self._statuses[article_id], file_object)
        except FileNotFoundError:
            print(file_path + " not found. ")

    def reload_article(self, article_id, article, findings):
        self._articles[article_id] = ArticleData(dict(article=article, findings=findings))

        if article_id in self._valid_dois_with_findings:
            self._valid_dois_with_findings.remove(article_id)

        if article_id in self._valid_dois_without_findings:
            self._valid_dois_without_findings.remove(article_id)

        if article_id in self._invalid_dois:
            self._invalid_dois.remove(article_id)

        self._assign_to_category(self._articles[article_id], article_id)

