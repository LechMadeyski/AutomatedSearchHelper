import pytest
from .ArticleData import ArticleData
from copy import deepcopy
import cattr

def test_merge_ArticleData_should_properly_merge_missing_data():
    emtpy_data = ArticleData()
    full_data = ArticleData(title="x",
                            doi='z',
                            publisher='w',
                            publisher_link='n',
                            scopus_link='e',
                            journal_info='q',
                            text=['something'],
                            authors=['quth'],
                            issn=['ewe'],
                            read_status='OK',
                            publish_year='1234',
                            journal_name='r')
    emtpy_data.merge(full_data)
    assert emtpy_data == full_data


def test_not_merge_if_already_filled():
    first_data = ArticleData(title="1",
                             doi='2',
                             publisher='3',
                             publisher_link='4',
                             scopus_link='5',
                             journal_info='6',
                             authors=['8'],
                             issn=['9'],
                             read_status='10',
                             publish_year='123',
                             journal_name='11')

    copied_first = deepcopy(first_data)

    full_data = ArticleData(title="x",
                            doi='z',
                            publisher='w',
                            publisher_link='n',
                            scopus_link='e',
                            journal_info='q',
                            authors=['quth'],
                            issn=['ewe'],
                            read_status='OK',
                            publish_year='555',
                            journal_name='r')
    first_data.merge(full_data)
    assert first_data == copied_first


def test_merge_ArticleData_should_properly_merge_all_missing_sections():
    first_data = ArticleData(text=[dict(
        title='Abstract',
        paragraphs=[dict(sentences='some some')]
    )])

    second_data = ArticleData(text=[
        dict(title='Any title2',
             paragraphs=[dict(sentences='anything')]),
        dict(title='Abstract',
             paragraphs=[dict(sentences='some some')]),
        dict(title='Any title',
             paragraphs=[dict(sentences='anything')])
    ])

    first_data.merge(second_data)

    assert first_data == ArticleData(text=[
        dict(title='Abstract',
             paragraphs=[dict(sentences='some some')]),
        dict(title='Any title2',
             paragraphs=[dict(sentences='anything')]),
        dict(title='Any title',
             paragraphs=[dict(sentences='anything')])
    ])


def test_create_ArticleData_from_dict():
    my_dict = {
        "authors": [
            "Pinheiro P.",
            "Viana J.C.",
            "Ribeiro M.",
            "Fernandes L.",
            "Ferrari F.",
            "Gheyi R.",
            "Fonseca B."
        ],
        "doi": "10.1016/j.scico.2020.102418\n",
        "end_page": "",
        "filename_base": "scopus_link_2-s2.0-85079538573",
        "issn": "01676423",
        "issue": "",
        "journal_info": "Volume 191, 1 June 2020, Article number 0102418",
        "journal_name": "Science of Computer Programming",
        "publish_year": "2020",
        "publisher": "Elsevier B.V.",
        "publisher_link": "",
        "read_status": "",
        "start_page": "",
        "text": [
            {
                "paragraphs": [
                    {
                        "sentences": [
                            "Mutation testing injects code changes to check whether tests can detect them.",
                            "Mutation testing tools use mutation operators that modify program elements such as operators, names, and entire statements.",
                            "Most existing mutation operators focus on imperative and object-oriented language constructs.",
                            "However, many current projects use meta-programming through code annotations.",
                            "In a previous work, we have proposed nine mutation operators for code annotations focused on the Java programming language.",
                            "In this article, we extend our previous work by mapping the operators to the C# language.",
                            "Moreover, we enlarge the empirical evaluation.",
                            "In particular, we mine Java and C# projects that make heavy use of annotations to identify annotation-related faults.",
                            "We analyzed 200 faults and categorized them as “misuse,” when the developer did not appear to know how to use the code annotations properly, and “wrong annotation parsing” when the developer incorrectly parsed annotation code (by using reflection, for example).",
                            "Our operators mimic 95% of the 200 mined faults.",
                            "In particular, three operators can mimic 82% of the faults in Java projects and 84% of the faults in C# projects.",
                            "In addition, we provide an extended and improved repository hosted on GitHub with the 200 code annotation faults we analyzed.",
                            "We organize the repository according to the type of errors made by the programmers while dealing with code annotations, and to the mutation operator that can mimic the faults.",
                            "Last but not least, we also provide a mutation engine, based on these operators, which is publicly available and can be incorporated into existing or new mutation tools.",
                            "The engine works for Java and C#.",
                            "As implications for practice, our operators can help developers to improve test suites and parsers of annotated code.",
                            "© 2020 Elsevier B.V."
                        ]
                    }
                ],
                "title": "Abstract"
            }
        ],
        "title": "Mutating code annotations: An empirical evaluation on Java and C# programs",
        "volume": "191"
    }

    # my_dict = dict(title='TTT', doi='some/doi')
    data = cattr.structure(my_dict, ArticleData)

    # assert data == ArticleData(title='TTT', doi='some/doi')
