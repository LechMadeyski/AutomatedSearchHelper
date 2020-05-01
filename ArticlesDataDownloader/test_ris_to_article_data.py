import pytest
from .ArticleData import ArticleData
from .ris_to_article_data import ris_to_article_data

def test_properly_read_full_article_data():
    ris_parts = [
        'TI  - Some long title title',
        'AU  - Author One',
        'AU  - Author Two',
        'DO  - 123.123/123',
        'AB  - Some sentence 1. Other sentence.',
        'PB  - Any Publisher',
        'JO  - Some journal name',
        'Y1  - 20 some date 20',
        'PY  - 1002',
        'SN  - Some issn'
    ]

    file_path = 'test_file.ris'
    with open(file_path, 'w') as file:
        file.write('TY  - SER\n')
        for part in ris_parts:
            file.write(part + '\n')
        file.write('ER  -  \n')

    assert ris_to_article_data(file_path) == ArticleData(
        doi='123.123/123',
        title='Some long title title',
        text=[dict(title='Abstract', paragraphs=[dict(sentences=['Some sentence 1.', 'Other sentence.'])])],
        journal_name='Some journal name',
        journal_info='',
        authors=['Author One', 'Author Two'],
        publisher='Any Publisher',
        issn='Some issn',
        publication_date='20 some date 20',
        scopus_link='',
        publisher_link=str(),
        read_status='',
        filename_base='123.123_123',
        publish_year='1002')
