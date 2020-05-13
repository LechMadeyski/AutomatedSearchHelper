from ArticlesDataDownloader.ACM.read_acm_bib import read_acm_bib
from ArticlesDataDownloader.IEEE.read_ieee_csv import read_ieee_csv
from ArticlesDataDownloader.InputSourceType import InputSourceType
from ArticlesDataDownloader.ScienceDirect.read_science_direct_ris import read_science_direct_ris
from ArticlesDataDownloader.Scopus.read_scopus_csv import read_scopus_csv
from ArticlesDataDownloader.Springer.read_springer_csv import read_springer_csv
from ArticlesDataDownloader.Willey.read_willey_ris import read_willey_ris


def read_input_file(filepath, source_type):
    if source_type == InputSourceType.SCOPUS_CSV:
        return read_scopus_csv(filepath)
    elif source_type == InputSourceType.IEEE_CSV:
        return read_ieee_csv(filepath)
    elif source_type == InputSourceType.SCIENCE_DIRECT_RIS:
        return read_science_direct_ris(filepath)
    elif source_type == InputSourceType.WILLEY_RIS:
        return read_willey_ris(filepath)
    elif source_type == InputSourceType.SPRINGER_CSV:
        return read_springer_csv(filepath)
    elif source_type == InputSourceType.ACM_BIB:
        return read_acm_bib(filepath)
    return None
