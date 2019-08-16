from TextSearchEngine.merge_findings import merge_findings


def find_in_sentece(sentence_text, matcher_function):
    findings = list()
    find_result = matcher_function(sentence_text)
    offset = 0
    while find_result is not None:
        findings.append((offset + find_result[0], offset + find_result[1]))
        offset += find_result[1]
        sentence_text = sentence_text[find_result[1]:]
        find_result = matcher_function(sentence_text)
    findings = merge_findings(findings)
    return findings


def find_in_paragraph(paragraph_text, matcher_function):
    sentences_findings = list()
    for sentence_index, sentence in enumerate(paragraph_text["sentences"]):
        sentence_result = {'sentenceIndex': sentence_index, 'findings': find_in_sentece(sentence, matcher_function)}
        if sentence_result["findings"]:
            sentences_findings.append(sentence_result)
    return sentences_findings


def find_in_section(section_text, matcher_function):
    section_findings = list()
    for paragraph_index, paragraph_text in enumerate(section_text["paragraphs"]):
        paragraph_result = {"paragraphIndex": paragraph_index,
                           "sentences": find_in_paragraph(paragraph_text, matcher_function)}
        if paragraph_result["sentences"]:
            section_findings.append(paragraph_result)
    return section_findings


def find_in_text_json(text_json, matcher_function):
    result = list()
    for section_index, section in enumerate(text_json["text"]):
        section_result = {
            "sectionIndex": section_index,
            "paragraphs": find_in_section(section, matcher_function)}
        if len(section_result["paragraphs"]) > 0:
            result.append(section_result)

    if len(result) < 1:
        return None

    return result
