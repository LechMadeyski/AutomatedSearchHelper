from bs4 import BeautifulSoup

import logging

from ArticlesDataDownloader.text_utilities import format_text_and_split_into_sentences


def __add_paragraph_if_not_empty(container, text):
    if text and text.strip():
        container.append({"sentences": format_text_and_split_into_sentences(text)})


def __add_list_elements(container, element):
    for list_item in element.contents:
        if list_item.name == 'li':
            __add_paragraph_if_not_empty(container, list_item.text)


def __add_div_if_has_elements(container, element):
    for sub_element in element.contents:
        if sub_element.name == 'ul' or sub_element.name == 'ol':
            for list_item in sub_element.contents:
                if list_item.name == 'li':
                    __add_paragraph_if_not_empty(container, list_item.text)
        elif sub_element.name == 'p':
            __add_paragraph_if_not_empty(container, sub_element.text)
        else:
            __add_paragraph_if_not_empty(container, sub_element.string)


def __translate_subsection(element):
    subsection_title = str()
    subsecton_paragraphs = []
    for sub_element in element.contents:
        if sub_element.name == 'h2' or sub_element.name == 'h3':
            subsection_title = sub_element.string or str()
            subsecton_paragraphs.append({"sentences": [subsection_title]})
        elif sub_element.name == 'ul' or sub_element.name == 'ol':
            for list_item in sub_element.contents:
                if list_item.name == 'li':
                    __add_paragraph_if_not_empty(subsecton_paragraphs, list_item.text)
        elif sub_element.name == 'p':
            __add_paragraph_if_not_empty(subsecton_paragraphs, sub_element.text)
        elif sub_element.name == 'div':
            __add_div_if_has_elements(subsecton_paragraphs, sub_element)
        else:
            __add_paragraph_if_not_empty(subsecton_paragraphs, sub_element.string)
    return {
        'title': subsection_title,
        'paragraphs': subsecton_paragraphs
    }


def willey_html_to_json(textHTML):
    logger = logging.getLogger("willeyHtmlToJson")
    logger.info("Start readig file")

    soup = BeautifulSoup(textHTML, "html.parser")

    outputJson = []

    for sec in soup.findAll(attrs={"class": "article-section__content"}):
        title = ''
        if not outputJson:
            title = "Abstract"  # first is always an abstract and has no text in h2(title)

        paragraphs = []
        subsections = []
        for element in sec.contents:
            if element.name == 'h2' or element.name == 'h3':
                title = element.string or str()
                paragraphs.append({"sentences": [title]})
            elif element.name == 'ul' or element.name == 'ol':
                __add_list_elements(paragraphs, element)
            elif element.name == 'section':
                subsections.append(__translate_subsection(element))
            elif element.name == 'p':
                __add_paragraph_if_not_empty(paragraphs, element.text)
            elif element.name == 'div':
                __add_div_if_has_elements(paragraphs, element)
            else:
                __add_paragraph_if_not_empty(paragraphs, element.string)

        logger.info("Reading section : " + title)
        secData = {
            'title': title,
            'paragraphs': paragraphs
        }
        outputJson.append(secData)
        outputJson += subsections

    if len(outputJson) < 3:
        raise SyntaxError('Could not read full text')

    return outputJson
