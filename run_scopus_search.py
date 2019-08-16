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




import requests
from pprint import pprint


#query = '"state+of+mutation+testing+at+google"'

query = 'TITLE-ABS-KEY("mutation+testing"+OR+"mutation+analysis"+AND+{C})'
#query = 'TITLE-ABS-KEY("mutation testing" OR "mutation analysis" OR "mutant analysis" AND {C} OR {C++} OR {C/C++}) AND (LIMIT-TO(SUBJAREA, "COMP")) AND (EXCLUDE(SUBJAREA, "BIOC"))',

#query = 'TITLE-ABS-KEY ( "mutation testing"  OR  "mutation analysis"  OR  "mutant analysis"  AND  {C}  OR  {C++}  OR  ' \
        # '{C/C++} )  AND  ( EXCLUDE ( SUBJAREA ,  "MEDI" )  OR  EXCLUDE ( SUBJAREA ,  "BIOC" ) )  AND  ( LIMIT-TO ( ' \
        # 'SUBJAREA ,  "COMP" ) ) '

#query_encoded ='%22mutation+testing%22+OR+%22mutation+analysis%22+OR+%22mutant+analysis%22+AND+%22C%22'
payload = {
    'query': query,
    'count': 120,
    #'date': '2018',
    'subj': 'COMP'
 #   'httpAccept': 'application/json',
#    'apiKey': '38c4f4e9143c11dccdc45ecbd58ec939'
}

headers = {
    'Accept': 'application/json',
    'X-ELS-APIKey': '38c4f4e9143c11dccdc45ecbd58ec939'
}
r= requests.get("https://api.elsevier.com/content/search/scopus",
                params=payload,
                headers=headers)

pprint(r.json())

results = r.json()["search-results"]

pprint("lenght = " + str(len(results['entry'])))

# for res in results['entry']:
#     pprint(res['dc:title'])

pprint(results['opensearch:Query'])


