# from pybliometrics.scopus import ScopusSearch

# import pybliometrics
# pybliometrics.scopus.utils.create_config()


# s = ScopusSearch(
#     "state of mutation testing",
#     # 'TITLE-ABS-KEY ( "mutation testing"  OR  "mutation analysis"  OR  "mutant analysis"  AND  {C}  OR  {C++}  OR  {'
#     # 'C/C++} )  AND  ( LIMIT-TO ( SUBJAREA ,  "COMP" ) )  AND  ( EXCLUDE ( SUBJAREA ,  "BIOC" ) )',
#     refresh=True)


#
# from pyscopus import Scopus
# key = '38c4f4e9143c11dccdc45ecbd58ec939'
# scopus = Scopus(key)
#
# res = scopus.search('TITLE-ABS-KEY("state of mutation testing")')




from pybliometrics.scopus import AbstractRetrieval
ab = AbstractRetrieval("2-s2.0-84930616647", view='FULL')

