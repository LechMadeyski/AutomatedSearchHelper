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
    filename, result_data = setup_downloader.readArticle(DOI, '')
    # TODO: add other bibliographic data - failing for now basing on ris

    assert filename == TEST_DIRECTORY + '/10.1016_j.ins.2019.08.077.json'
    assert result_data['read_status'] == 'OK'
    assert result_data['title'] == 'ABFL: An autoencoder based practical approach for software fault localization'
    assert result_data['doi'] == DOI
    assert len(result_data['authors']) == 6
    assert len(result_data['text']) == 31
    assert 'Abstract' in result_data['text'][0]['title']
    assert len(result_data['text'][0]['paragraphs']) == 1
    assert len(result_data['text'][0]['paragraphs'][0]['sentences']) == 9
    assert 'Introduction' in result_data['text'][1]['title']
    assert 'Background' in result_data['text'][2]['title']
    assert 'Spectrum Based Fault Localization' in result_data['text'][3]['title']
    assert len(result_data['text'][3]['paragraphs'][0]['sentences']) == 3
    assert 'Conclusion and future work' in result_data['text'][-3]['title']
    assert 'Declaration of Competing Interest' in result_data['text'][-2]['title']
    assert 'Acknowledgments' in result_data['text'][-1]['title']

def test_springer_html_by_doi(setup_downloader):
    DOI = '10.1007/978-3-030-38364-0_32'
    filename, result_data = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1007_978-3-030-38364-0_32.json'
    assert result_data['publisher_link'] == 'http://link.springer.com/10.1007/978-3-030-38364-0_32'
    assert result_data['publish_year'] == '2020'

    assert result_data['read_status'] == 'OK'
    assert result_data['title'] == 'An Improvement of Applying Multi-objective Optimization Algorithm into Higher Order Mutation Testing'
    assert result_data['doi'] == DOI
    assert len(result_data['authors']) == 2
    assert len(result_data['text']) == 9
    assert result_data['text'][0]['title'] == 'Abstract'
    assert len(result_data['text'][0]['paragraphs']) == 1
    assert len(result_data['text'][0]['paragraphs'][0]['sentences']) == 3
    assert 'Introduction' in result_data['text'][1]['title']
    assert len(result_data['text'][1]['paragraphs']) == 5
    assert len(result_data['text'][1]['paragraphs'][3]['sentences']) == 3
    assert 'Proposed Approach and Related Works' in result_data['text'][2]['title']
    assert 'Supporting Tool and PUTs' in result_data['text'][3]['title']
    assert 'Results Analysis' in result_data['text'][4]['title']
    assert 'Conclusions' in result_data['text'][5]['title']
    assert 'Notes' in result_data['text'][6]['title']


def test_willey_html_by_doi(setup_downloader):
    DOI = '10.1002/stvr.1728'
    filename, result_data = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1002_stvr.1728.json'
    assert result_data['publisher_link'] == 'https://onlinelibrary.wiley.com/doi/abs/10.1002/stvr.1728'
    assert result_data['publish_year'] == '2020'

    assert result_data['read_status'] == 'OK'
    assert result_data['title'] == 'Performance mutation testing'
    assert result_data['doi'] == DOI
    assert len(result_data['authors']) == 4
    assert len(result_data['text']) == 12
    assert result_data['text'][0]['title'] == 'Abstract'
    assert len(result_data['text'][0]['paragraphs']) == 1
    assert len(result_data['text'][0]['paragraphs'][0]['sentences']) == 11
    assert 'Introduction' in result_data['text'][1]['title']
    assert len(result_data['text'][1]['paragraphs']) == 6
    assert len(result_data['text'][1]['paragraphs'][3]['sentences']) == 7
    assert 'Background' in result_data['text'][2]['title']
    assert 'Problem Statement' in result_data['text'][3]['title']
    assert 'Research Questions' in result_data['text'][4]['title']
    assert 'Performance Mutation Operators' in result_data['text'][5]['title']
    assert 'Evaluation' in result_data['text'][6]['title']
    assert 'Conclusion and Future Work' in result_data['text'][-2]['title']
    assert 'Acknowledgements' in result_data['text'][-1]['title']



def test_ieee_html_by_doi(setup_downloader):
    DOI = '10.1109/APSEC48747.2019.00022'
    filename, result_data = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1109_APSEC48747.2019.00022.json'
    assert result_data['publisher_link'] == 'https://ieeexplore.ieee.org/document/8946088/'

    assert result_data['publish_year'] == '2019'

    assert result_data['read_status'] == 'OK'
    assert result_data['title'] == 'A Mutation-Based Approach for Assessing Weight Coverage of a Path Planner'
    assert result_data['doi'] == DOI
    assert len(result_data['authors']) == 4
    assert len(result_data['text']) == 9
    assert result_data['text'][0]['title'] == 'Abstract'
    assert len(result_data['text'][0]['paragraphs']) == 1
    assert len(result_data['text'][0]['paragraphs'][0]['sentences']) == 7
    assert 'Introduction' in result_data['text'][1]['title']
    assert len(result_data['text'][1]['paragraphs']) == 12
    assert len(result_data['text'][1]['paragraphs'][6]['sentences']) == 5
    assert 'Definitions' in result_data['text'][2]['title']
    assert 'Proposed Approach' in result_data['text'][3]['title']
    assert 'Experiments' in result_data['text'][4]['title']
    assert 'Discussion' in result_data['text'][5]['title']
    assert 'Threats To Validity' in result_data['text'][6]['title']
    assert 'Related Work' in result_data['text'][7]['title']
    assert 'Conclusions' in result_data['text'][8]['title']


def test_acm_pdf_by_doi(setup_downloader):
    DOI = '10.1145/3293882.3330574'
    filename, result_data = setup_downloader.readArticle(DOI, '')

    assert filename == TEST_DIRECTORY + '/10.1145_3293882.3330574.json'
    assert result_data['publisher_link'] == 'http://dl.acm.org/citation.cfm?doid=3293882.3330574'
   # assert result_data['publish_year'] == '2019'

    assert result_data['read_status'] == 'OK'
    assert result_data['title'] == 'DeepFL: integrating multiple fault diagnosis dimensions for deep fault localization'
    assert result_data['doi'] == DOI
    assert len(result_data['authors']) == 4
    assert len(result_data['text']) == 9
    assert result_data['text'][0]['title'] == 'Begining data'
    assert result_data['text'][1]['title'] == 'ABSTRACT'
    assert len(result_data['text'][1]['paragraphs']) == 1
    assert len(result_data['text'][1]['paragraphs'][0]['sentences']) == 25
    assert 'INTRODUCTION' in result_data['text'][2]['title']
    assert len(result_data['text'][2]['paragraphs']) == 1
    assert len(result_data['text'][2]['paragraphs'][0]['sentences']) == 33
    assert 'BACKGROUND AND RELATED WORK' in result_data['text'][3]['title']
    assert 'APPROACH' in result_data['text'][4]['title']
    assert 'EXPERIMENTAL SETUP' in result_data['text'][5]['title']
    assert 'RESULT ANALYSIS' in result_data['text'][6]['title']
    assert 'CONCLUSION' in result_data['text'][7]['title']
    assert 'REFERENCES' in result_data['text'][8]['title']


def test_article_with_scopus_link_only(setup_downloader):
    SCOPUS_LINK = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-85074719668&origin=inward&txGid=743ab63d74ada4f8f3059ad6e752522e'
    filename, result_data = setup_downloader.readArticle('anyName', SCOPUS_LINK)

    assert filename == TEST_DIRECTORY + '/anyName.json'












#Already has file

#IEEE test text
#IEEE test pdf etc..
#Scopus test