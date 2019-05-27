from TextSearchEngine.searchFunctions import *

finder = AND(EXACT_WORD("mutation testing"), EXACT_WORD("C", caseSensitive = True), AND(PARTIAL_WORD("e")))
