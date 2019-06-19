from TextSearchEngine.searchFunctions import *

finder = AND(
    PARTIAL_WORD("mutation testing"),
    OR(
        EXACT_WORD("C", caseSensitive = True),
        EXACT_WORD("LLVM", caseSensitive = True)))
