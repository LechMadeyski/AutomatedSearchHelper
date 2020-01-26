from enum import IntEnum


class ArticleStatus(IntEnum):
    READ_CORRECT_WITH_FINDINGS = 1,
    READ_PARTIAL_WITH_FINDINGS = 2,
    READ_PARTIAL_NO_FINDINGS = 3,
    READ_CORRECT_NO_FINDINGS = 4,
