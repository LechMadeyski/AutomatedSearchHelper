from enum import IntEnum


class InputSourceType(IntEnum):
    SCOPUS_CSV = 1
    IEEE_CSV = 2
    SCIENCE_DIRECT_RIS = 3
    SPRINGER_RIS = 4
    ACM_BIB = 4
