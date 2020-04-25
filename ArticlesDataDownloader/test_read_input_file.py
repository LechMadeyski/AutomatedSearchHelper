import pytest
import os
import pathlib

from ArticlesDataDownloader.InputSourceType import InputSourceType
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.read_input_file import read_input_file


def test_shall_properly_read_scopus_csv():
    path_to_file = os.path.dirname(os.path.abspath(__file__)) + '/Scopus/scopus_full_test.csv'
    result = read_input_file(path_to_file, InputSourceType.SCOPUS_CSV)
    assert len(result) == 13
    assert result[9] == ArticleData(
        doi='10.1007/978-3-030-41418-4_13',
        scopus_link='https://www.scopus.com/inward/record.uri?eid=2-s2.0-85081574699&doi=10.1007%2f978-3-030-41418-4_13&partnerID=40&md5=ad97ee8faa7740ef780916251f27bff5',
        title='A new mutant generation algorithm based on basic path coverage for mutant reduction',
        authors=['Qin X.', 'Liu S.', 'Tao Z.'],
        publish_year='2020',
        publisher='Springer',
        journal_name='Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics)',
        volume='12028 LNCS',
        issue='5',
        start_page='167',
        end_page='186',
        issn='03029743',
        filename_base='10.1007_978-3-030-41418-4_13',
        text=[dict(title='Abstract', paragraphs=[dict(sentences=['Simple abstract.', 'Two sentences.'])])])
    article_without_doi = result[0]
    assert article_without_doi.filename_base == 'scopus_link_2-s2.0-85079538573'


def test_shall_properly_read_ieee_csv():
    path_to_file = os.path.dirname(os.path.abspath(__file__)) + '/IEEE/ieee_test.csv'
    result = read_input_file(path_to_file, InputSourceType.IEEE_CSV)
    assert len(result) == 25
    assert result[8] == ArticleData(
        doi='10.1109/SNPD.2015.7176242',
        title='Overview of a place/transition net-based mutation testing framework to obtain test cases effective for concurrent software',
        authors=['T. Takagi', 'T. Arao'],
        publish_year='2015',
        publisher='IEEE',
        journal_name='2015 IEEE/ACIS 16th International Conference on Software Engineering, Artificial Intelligence, Networking and Parallel/Distributed Computing (SNPD)',
        volume='33',
        issue='22',
        start_page='1',
        end_page='3',
        issn='SOMEISSSN',
        publisher_link='https://ieeexplore.ieee.org/document/7176242',
        filename_base='10.1109_SNPD.2015.7176242',
        text=[dict(title='Abstract', paragraphs=[dict(sentences=['Any abstract.', 'Two sentences.'])])])

    missing_doi_article = result[20]
    assert missing_doi_article.filename_base == 'IEEE_8449437'


def test_shall_properly_read_science_direct_ris():
    path_to_file = os.path.dirname(os.path.abspath(__file__)) + '/ScienceDirect/science_direct_test.ris'
    result = read_input_file(path_to_file, InputSourceType.SCIENCE_DIRECT_RIS)
    assert len(result) == 25
    assert result[8] == ArticleData(
        doi='10.1016/j.scico.2016.01.003',
        title='Model-based mutation testing—Approach and case studies',
        authors=['Belli, Fevzi', 'Budnik, Christof J.'],
        publish_year='2016',
        publisher='Science Direct',
        journal_name='Science of Computer Programming',
        volume='120',
        issue='22',
        start_page='25',
        end_page='48',
        issn='0167-6423',
        publisher_link='http://www.sciencedirect.com/science/article/pii/S0167642316000137',
        filename_base='10.1016_j.scico.2016.01.003',
        text=[dict(title='Abstract', paragraphs=[dict(sentences=['Some abstract.', 'Two sentences.'])])])
    article_without_doi = result[0]
    assert article_without_doi.filename_base == 'science_direct_S0950584916300246'


def test_shall_properly_read_willey_ris():
    path_to_file = os.path.dirname(os.path.abspath(__file__)) + '/Willey/willey_test.ris'
    result = read_input_file(path_to_file, InputSourceType.WILLEY_RIS)
    assert len(result) == 20
    assert result[4] == ArticleData(
        doi='10.1002/stvr.1531',
        title='Model-based mutation testing from security protocols in HLPSL',
        authors=['Dadeau, Frédéric', 'Héam, Pierre-Cyrille', 'Kheddam, Rafik', 'Maatoug, Ghazi', 'Rusinowitch, Michael'],
        publish_year='2015',
        publisher='John Wiley & Sons, Ltd',
        journal_name='Software Testing, Verification and Reliability',
        volume='25',
        issue='5-7',
        start_page='684',
        end_page='711',
        issn='0960-0833',
        filename_base='10.1002_stvr.1531',
        publisher_link='https://doi.org/10.1002/stvr.1531',
        text=[dict(title='Abstract', paragraphs=[dict(sentences=['Any abstract.', 'Two sentences.'])])])


def test_shall_properly_read_springer_csv():
    path_to_file = os.path.dirname(os.path.abspath(__file__)) + '/Springer/springer_test.csv'
    result = read_input_file(path_to_file, InputSourceType.SPRINGER_CSV)
    assert len(result) == 9
    assert result[3] == ArticleData(
        doi='10.1007/978-3-662-49381-6_23',
        filename_base='10.1007_978-3-662-49381-6_23',
        title='Higher Order Mutation Testing to Drive Development of New Test Cases: An Empirical Comparison of Three Strategies',
        publish_year='2016',
        journal_name='Intelligent Information and Database Systems',
        publisher_link='http://link.springer.com/chapter/10.1007/978-3-662-49381-6_23')
