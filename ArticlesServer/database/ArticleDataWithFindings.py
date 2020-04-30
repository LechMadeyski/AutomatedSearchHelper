from .ArticleStatus import ArticleStatus


class ArticleDataWithFindings:
    def __init__(self, article_and_finding_json):
        self._article_data = article_and_finding_json.get('article', dict())
        self._findings = article_and_finding_json.get('findings', [])
        self._search_base = article_and_finding_json.get('base_article_data', None)
        self._is_ignored = False

    def toggle_ignored(self):
        self._is_ignored = not self._is_ignored

    @property
    def title(self):
        return self._article_data.get('title', str())

    @property
    def authors(self):
        return self._article_data.get('authors', list())

    @property
    def read_status(self):
        return self._article_data.get('read_status', "Cannot read")

    @property
    def journal_name(self):
        return self._article_data.get('journalName', str()) or self._article_data.get('journal_name', str())

    @property
    def journal_info(self):
        return self._article_data.get('journalInfo', str()) or self._article_data.get('journal_info', str())

    @property
    def publisher(self):
        return self._article_data.get('publisher', str())

    @property
    def issn(self):
        return self._article_data.get('issn', str())

    @property
    def scopus_link(self):
        return self._article_data.get('scopus_link', str())

    @property
    def doi_link(self):
        if 'scopus' in self.doi or self.doi == str():
            return str()
        else:
            return 'http://doi.org/' + self.doi

    @property
    def doi(self):
        return self._article_data.get('doi', str())

    @property
    def publisher_link(self):
        return self._article_data.get('publisher_link', str())

    @property
    def text(self):
        return self._article_data.get('text', list())

    @property
    def findings(self):
        return self._findings

    @property
    def read_error(self):
        error_status = self._article_data.get('read_status', str())
        if error_status != 'OK':
            if error_status == str():
                return 'Undefined error'
            else:
                return error_status
        return str()

    @property
    def status(self):
        if self._is_ignored:
            return ArticleStatus.ARTICLE_IGNORED
        if self.read_status == 'OK':
            if self.findings:
                return ArticleStatus.READ_CORRECT_WITH_FINDINGS
            else:
                return ArticleStatus.READ_CORRECT_NO_FINDINGS
        else:
            if self.findings:
                return ArticleStatus.READ_PARTIAL_WITH_FINDINGS
            elif self.read_status == 'Publisher not supported':
                return ArticleStatus.READ_PARTIAL_PUBLISHER_NOT_SUPPORTED_NO_FINDINGS
            else:
                return ArticleStatus.READ_PARTIAL_ERROR_READING_NO_FINDINGS

    @property
    def search_base(self):
        return self._search_base
