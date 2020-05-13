import attr


@attr.s
class ArticleData:
    doi = attr.ib(default=str())
    title = attr.ib(default=str())
    text = attr.ib(default=list())
    journal_name = attr.ib(default=str())
    journal_info = attr.ib(default=str())
    authors = attr.ib(default=list())
    publisher = attr.ib(default=str())
    issn = attr.ib(default=str())
    scopus_link = attr.ib(default=str())
    publisher_link = attr.ib(default=str())
    read_status = attr.ib(default=str())
    publish_year = attr.ib(default=str())
    volume = attr.ib(default=str())
    issue = attr.ib(default=str())
    start_page = attr.ib(default=str())
    end_page = attr.ib(default=str())
    publication_date = attr.ib(default=str())
    filename_base = attr.ib(default=str())

    def to_dict(self):
        return attr.asdict(self)

    def merge(self, other):
        if not self.doi:
            self.doi = other.doi
        if not self.title:
            self.title = other.title
        if not self.journal_name:
            self.journal_name = other.journal_name
        if not self.journal_info:
            self.journal_info = other.journal_info
        if not self.authors:
            self.authors = other.authors
        if not self.publisher:
            self.publisher = other.publisher
        if not self.issn:
            self.issn = other.issn
        if not self.scopus_link:
            self.scopus_link = other.scopus_link
        if not self.publish_year:
            self.publish_year = other.publish_year
        if not self.publisher_link:
            self.publisher_link = other.publisher_link
        if not self.read_status:
            self.read_status = other.read_status
        if not self.volume:
            self.volume = other.volume
        if not self.issue:
            self.issue = other.issue
        if not self.start_page:
            self.start_page = other.start_page
        if not self.end_page:
            self.end_page = other.end_page
        if not self.filename_base:
            self.filename_base = other.filename_base
        if not self.publication_date:
            self.publication_date = other.publication_date

        if not self.text:
            self.text = other.text
        elif other.text:
            result_text = [x for x in self.text]
            for section in other.text:
                if not [x for x in self.text if x['title'].lower() == section['title'].lower()]:
                    result_text.append(section)
            self.text = result_text



