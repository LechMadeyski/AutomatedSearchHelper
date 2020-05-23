from enum import IntEnum


class InputSourceType(IntEnum):
    SCOPUS_CSV = 1
    IEEE_CSV = 2
    SCIENCE_DIRECT_RIS = 3
    SPRINGER_CSV = 4
    WILLEY_RIS = 5
    WILLEY_BIB = 6
    ACM_BIB = 7
