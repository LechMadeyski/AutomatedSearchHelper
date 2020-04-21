from ArticlesDataDownloader.IEEE.read_ieee_csv import read_ieee_csv
from ArticlesDataDownloader.InputSourceType import InputSourceType
from ArticlesDataDownloader.ScienceDirect.read_science_direct_ris import read_science_direct_ris
from ArticlesDataDownloader.Scopus.read_scopus_csv import read_scopus_csv

def read_input_file(filepath, source_type):
    if source_type == InputSourceType.SCOPUS_CSV:
        return read_scopus_csv(filepath)
    elif source_type == InputSourceType.IEEE_CSV:
        return read_ieee_csv(filepath)
    elif source_type == InputSourceType.SCIENCE_DIRECT_RIS:
        return read_science_direct_ris(filepath)
    return None
