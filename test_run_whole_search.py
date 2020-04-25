import pytest
import os

from run_whole_search import main


def test_run_scopus():
    result = os.system('python run_whole_search.py --file_type=1 --articles_list=ArticlesDataDownloader/Scopus/scopus_full_test.csv')
    assert result == 0


def test_run_ieee():
    result = os.system('python run_whole_search.py --file_type=2 --articles_list=ArticlesDataDownloader/IEEE/ieee_test.csv')
    assert result == 0


def test_run_science_direct():
    result = os.system('python run_whole_search.py --file_type=3 --articles_list=ArticlesDataDownloader/ScienceDirect/science_direct_test.ris')
    assert result == 0


def test_run_springer():
    result = os.system('python run_whole_search.py --file_type=4 --articles_list=ArticlesDataDownloader/Springer/springer_test.csv')
    assert result == 0


def test_run_willey():
    result = os.system('python run_whole_search.py --file_type=5 --articles_list=ArticlesDataDownloader/Willey/willey_test.ris')
    assert result == 0

