import pytest
import os
import shutil
from .ArticlesDataDownloader import ArticlesDataDownloader

TEST_DIRECTORY = ".test_directory"

SHOULD_CLEAR = False

@pytest.fixture
def setup_downloader(should_clear = SHOULD_CLEAR):
    if should_clear:
        if os.path.exists(TEST_DIRECTORY):
            shutil.rmtree(TEST_DIRECTORY)
        os.makedirs(TEST_DIRECTORY)
    elif not os.path.exists(TEST_DIRECTORY):
        os.makedirs(TEST_DIRECTORY)
    downloader = ArticlesDataDownloader(TEST_DIRECTORY, 'proxy_auth_plugin.zip')
    yield downloader
    if should_clear:
        shutil.rmtree(TEST_DIRECTORY)


def test_science_direct_html_by_doi(setup_downloader):
    DOI = "10.1016/j.ins.2019.08.077"
    filename, resultData = setup_downloader.readArticle(DOI, '')
    # TODO: add other bibliographic data - failing for now basing on ris

    assert filename == TEST_DIRECTORY + '/10.1016_j.ins.2019.08.077.json'
    assert resultData['read_status'] == 'OK'
    assert resultData['title'] == 'ABFL: An autoencoder based practical approach for software fault localization'
    assert resultData['doi'] == DOI
    assert len(resultData['authors']) == 6
    assert len(resultData['text']) == 31
    assert 'Abstract' in resultData['text'][0]['title']
    assert len(resultData['text'][0]['paragraphs']) == 1
    assert len(resultData['text'][0]['paragraphs'][0]['sentences']) == 9
    assert 'Introduction' in resultData['text'][1]['title']
    assert 'Background' in resultData['text'][2]['title']
    assert 'Spectrum Based Fault Localization' in resultData['text'][3]['title']
    assert len(resultData['text'][3]['paragraphs'][0]['sentences']) == 3
    assert 'Conclusion and future work' in resultData['text'][-3]['title']
    assert 'Declaration of Competing Interest' in resultData['text'][-2]['title']
    assert 'Acknowledgments' in resultData['text'][-1]['title']

def test_springer_html_by_doi(setup_downloader):
    DOI = '10.1007/978-3-030-38364-0_32'
    filename, resultData = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1007_978-3-030-38364-0_32.json'
    assert resultData['publisher_link'] == 'http://link.springer.com/10.1007/978-3-030-38364-0_32'
    assert resultData['publish_year'] == '2020'

    assert resultData['read_status'] == 'OK'
    assert resultData['title'] == 'An Improvement of Applying Multi-objective Optimization Algorithm into Higher Order Mutation Testing'
    assert resultData['doi'] == DOI
    assert len(resultData['authors']) == 2
    assert len(resultData['text']) == 9
    assert resultData['text'][0]['title'] == 'Abstract'
    assert len(resultData['text'][0]['paragraphs']) == 1
    assert len(resultData['text'][0]['paragraphs'][0]['sentences']) == 3
    assert 'Introduction' in resultData['text'][1]['title']
    assert len(resultData['text'][1]['paragraphs']) == 5
    assert len(resultData['text'][1]['paragraphs'][3]['sentences']) == 3
    assert 'Proposed Approach and Related Works' in resultData['text'][2]['title']
    assert 'Supporting Tool and PUTs' in resultData['text'][3]['title']
    assert 'Results Analysis' in resultData['text'][4]['title']
    assert 'Conclusions' in resultData['text'][5]['title']
    assert 'Notes' in resultData['text'][6]['title']


def test_willey_html_by_doi(setup_downloader):
    DOI = '10.1002/stvr.1728'
    filename, resultData = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1002_stvr.1728.json'
    assert resultData['read_status'] == 'OK'
    assert resultData['title'] == 'Performance mutation testing'
    assert resultData['doi'] == DOI
    assert len(resultData['authors']) == 4
    assert len(resultData['text']) == 12
    assert resultData['text'][0]['title'] == 'Abstract'
    assert len(resultData['text'][0]['paragraphs']) == 1
    assert len(resultData['text'][0]['paragraphs'][0]['sentences']) == 11
    assert 'Introduction' in resultData['text'][1]['title']
    assert len(resultData['text'][1]['paragraphs']) == 6
    assert len(resultData['text'][1]['paragraphs'][3]['sentences']) == 7
    assert 'Background' in resultData['text'][2]['title']
    assert 'Problem Statement' in resultData['text'][3]['title']
    assert 'Research Questions' in resultData['text'][4]['title']
    assert 'Performance Mutation Operators' in resultData['text'][5]['title']
    assert 'Evaluation' in resultData['text'][6]['title']
    assert 'Conclusion and Future Work' in resultData['text'][-2]['title']
    assert 'Acknowledgements' in resultData['text'][-1]['title']



def test_willey_ieee_by_doi(setup_downloader):
    DOI = '10.1109/APSEC48747.2019.00022'
    filename, resultData = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1109_APSEC48747.2019.00022.json'
    assert resultData['read_status'] == 'OK'
    assert resultData['title'] == 'A Mutation-Based Approach for Assessing Weight Coverage of a Path Planner'
    assert resultData['doi'] == DOI
    assert len(resultData['authors']) == 4
    assert len(resultData['text']) == 9
    assert resultData['text'][0]['title'] == 'Abstract'
    assert len(resultData['text'][0]['paragraphs']) == 1
    assert len(resultData['text'][0]['paragraphs'][0]['sentences']) == 7
    assert 'Introduction' in resultData['text'][1]['title']
    assert len(resultData['text'][1]['paragraphs']) == 12
    assert len(resultData['text'][1]['paragraphs'][6]['sentences']) == 5
    assert 'Definitions' in resultData['text'][2]['title']
    assert 'Proposed Approach' in resultData['text'][3]['title']
    assert 'Experiments' in resultData['text'][4]['title']
    assert 'Discussion' in resultData['text'][5]['title']
    assert 'Threats To Validity' in resultData['text'][6]['title']
    assert 'Related Work' in resultData['text'][7]['title']
    assert 'Conclusions' in resultData['text'][8]['title']


def test_acm_pdf_by_doi(setup_downloader):
    DOI = '10.1145/3293882.3330574'
    filename, resultData = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1145_3293882.3330574.json'
    assert resultData['read_status'] == 'OK'
    assert resultData['title'] == 'DeepFL: integrating multiple fault diagnosis dimensions for deep fault localization'
    assert resultData['doi'] == DOI
    assert len(resultData['authors']) == 4
    assert len(resultData['text']) == 9
    assert resultData['text'][0]['title'] == 'Begining data'
    assert resultData['text'][1]['title'] == 'ABSTRACT'
    assert len(resultData['text'][1]['paragraphs']) == 1
    assert len(resultData['text'][1]['paragraphs'][0]['sentences']) == 25
    assert 'INTRODUCTION' in resultData['text'][2]['title']
    assert len(resultData['text'][2]['paragraphs']) == 1
    assert len(resultData['text'][2]['paragraphs'][0]['sentences']) == 33
    assert 'BACKGROUND AND RELATED WORK' in resultData['text'][3]['title']
    assert 'APPROACH' in resultData['text'][4]['title']
    assert 'EXPERIMENTAL SETUP' in resultData['text'][5]['title']
    assert 'RESULT ANALYSIS' in resultData['text'][6]['title']
    assert 'CONCLUSION' in resultData['text'][7]['title']
    assert 'REFERENCES' in resultData['text'][8]['title']


def test_article_with_scopus_link_only(setup_downloader):
    SCOPUS_LINK = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-85074719668&origin=inward&txGid=743ab63d74ada4f8f3059ad6e752522e'
    filename, resultData = setup_downloader.readArticle('anyName', SCOPUS_LINK)

    assert filename == TEST_DIRECTORY + '/anyName.json'












#Already has file

#IEEE test text
#IEEE test pdf etc..
#Scopus test