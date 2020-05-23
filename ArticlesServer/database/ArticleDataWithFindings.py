import os

from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesServer.directories import OUTPUT_DIRECTORY
from .ArticleStatus import ArticleStatus


class ArticleDataWithFindings:
    def __init__(self, article_and_finding_json):
        self._article_data = article_and_finding_json.get('article_data', ArticleData)
        self._findings = article_and_finding_json.get('findings', [])
        self._search_base = article_and_finding_json.get('base_article_data', None)
        self._is_ignored = False

    def toggle_ignored(self):
        self._is_ignored = not self._is_ignored

    @property
    def title(self):
        return self._article_data.title

    @property
    def authors(self):
        return self._article_data.authors

    @property
    def read_status(self):
        return self._article_data.read_status

    @property
    def journal_name(self):
        return self._article_data.journal_name

    @property
    def journal_info(self):
        result = str()

        if self._article_data.volume:
            result += 'Volume: ' + self._article_data.volume + ' '

        if self._article_data.issue:
            result += 'Issue: ' + self._article_data.issue + ' '

        if self._article_data.start_page and self._article_data.end_page:
            result += self._article_data.start_page + '-' + self._article_data.end_page + ' '

        if self._article_data.publication_date:
            result += 'Published : ' + self._article_data.publication_date + ' '
        elif self._article_data.publish_year:
            result += 'Published : ' + self._article_data.publish_year + ' '

        return result

    @property
    def publisher(self):
        return self._article_data.publisher

    @property
    def issn(self):
        return self._article_data.issn

    @property
    def scopus_link(self):
        return self._article_data.scopus_link

    @property
    def doi_link(self):
        if self._article_data.doi:
            return 'http://doi.org/' + self._article_data.doi
        else:
            return str()

    @property
    def doi(self):
        return self._article_data.doi

    @property
    def publisher_link(self):
        return self._article_data.publisher_link

    @property
    def text(self):
        return self._article_data.text

    @property
    def findings(self):
        return self._findings

    @property
    def read_error(self):
        error_status = self._article_data.read_status
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
        if 'OK' in self.read_status:
            if self.findings:
                return ArticleStatus.READ_CORRECT_WITH_FINDINGS
            elif self.read_status == 'OK':
                return ArticleStatus.READ_CORRECT_NO_FINDINGS
            elif self.read_status == 'OK - PDF READ':
                return ArticleStatus.READ_FROM_PDF_NO_FINDINGS
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

    def get_pdf_filename(self):
        pdf_filename = os.path.join(OUTPUT_DIRECTORY, self._article_data.filename_base + '.pdf')
        if os.path.isfile(pdf_filename):
            return pdf_filename
        else:
            return None

    @property
    def filename_base(self):
        return self._article_data.filename_base
