from .search_functions import *


def _get_leaf_parser_parameters(text, method_name):
    word_start = text.find('"')
    if word_start == -1 or word_start == len(text) - 1:
        raise ValueError("Could not find word start in " + method_name)
    word_end = text.find('"', word_start + 1)
    if word_end == -1:
        raise ValueError("Could not find word end in " + method_name)
    word = text[word_start + 1: word_end]

    method_end = text.find(')', word_end)

    if method_end == -1:
        raise ValueError("Could not find end of " + method_name)

    parameters = text[word_end + 1: method_end]
    case_sensitive = False
    if parameters.find('case_sensitive') != -1:
        case_sensitive = True

    return word, case_sensitive, method_end


def _get_node_matchers(analyzed_text, method_name):
    method_start = 0
    next_closer = analyzed_text.find(')')
    matchers = list()

    while analyzed_text[method_start:next_closer].replace(' ', '') != str():
        print('parsing finder from : ' + analyzed_text[method_start:])
        finder, method_end = _get_next_finder(analyzed_text[method_start:])
        matchers.append(finder)
        print('Got finder ' + str(finder))
        method_start = method_start + method_end + 1
        next_closer = analyzed_text.find(')', method_start)
        comma_pos = analyzed_text.find(',', method_start, next_closer)
        if comma_pos != -1:
            method_start = comma_pos + 1
        if next_closer == -1:
            raise ValueError("Missing closer in " + method_name)

    return matchers, next_closer

def _get_next_finder(text):
    index = text.find('(')

    if index == -1:
        raise ValueError("Could not find any ( at the beginning")

    method_name = text[:index].replace(' ', '')
    print("Analyzing method", method_name)

    insides_start = index+1

    if method_name == 'EXACT_WORD':
        word, case_sensitive, method_end = _get_leaf_parser_parameters(text[insides_start:], method_name)
        return EXACT_WORD(word, case_sensitive=case_sensitive), insides_start+method_end
    elif method_name == 'PARTIAL_WORD':
        word, case_sensitive, method_end = _get_leaf_parser_parameters(text[insides_start:], method_name)
        return PARTIAL_WORD(word, case_sensitive=case_sensitive), insides_start+method_end
    elif method_name == 'OR':
        matchers, method_end = _get_node_matchers(text[insides_start:], method_name)
        return OR(*matchers), method_end+insides_start
    elif method_name == 'AND':
        matchers, method_end = _get_node_matchers(text[insides_start:], method_name)
        return AND(*matchers), method_end+insides_start
    else:
        raise ValueError("Could not recognize proper method " + method_name)


def parse_finder(text):
    finder, _ = _get_next_finder(text)
    return finder
