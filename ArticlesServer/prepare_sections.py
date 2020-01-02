def find_matching_section(section_index, findings):
    found_sections = [x for x in findings if section_index == x["sectionIndex"]]
    if found_sections:
        return found_sections[0]
    return None


def find_matching_paragraph(paragraph_index, findings_section):
    found_paragraph = [x for x in findings_section['paragraphs'] if paragraph_index == x["paragraphIndex"]]
    if found_paragraph:
        return found_paragraph[0]
    return None


def find_matching_sentence(sentence_index, findings_paragraph):
    found_sentence = [x for x in findings_paragraph['sentences'] if sentence_index == x["sentenceIndex"]]
    if found_sentence:
        return found_sentence[0]
    return None


def prepare_sentence(sentence, findings_sentence=None):
    if findings_sentence:
        sentence_result = list()
        part_start_index = 0
        for finding in findings_sentence['findings']:
            if part_start_index is not finding[0]:
                sentence_result.append(dict(marked=False, text=sentence[part_start_index:finding[0]]))
            sentence_result.append(dict(marked=True, text=sentence[finding[0]:finding[1]]))
            part_start_index = finding[1]
        if part_start_index != len(sentence):
            sentence_result.append(dict(marked=False, text=sentence[part_start_index:]))
        return sentence_result
    else:
        return [dict(marked=False, text=sentence)]


def prepare_sentences(paragraph, findings_paragraph=None):
    if findings_paragraph:
        paragraph_result = list()
        sentences_bundle = dict(hidden=True, sentences=list())
        for sentence_index, sentence in enumerate(paragraph['sentences']):
            findings_sentence = find_matching_sentence(sentence_index, findings_paragraph)
            hidden = True if findings_sentence is None else False
            if sentences_bundle['hidden'] == hidden:
                sentences_bundle['sentences'].append(prepare_sentence(sentence, findings_sentence))
            else:
                if len(sentences_bundle['sentences']) > 0:
                    paragraph_result.append(sentences_bundle)
                sentences_bundle = dict(hidden=hidden, sentences=[prepare_sentence(sentence, findings_sentence)])
        if len(sentences_bundle['sentences']) > 0:
            paragraph_result.append(sentences_bundle)
        return paragraph_result
    else:
        res = dict(
            hidden=False,
            sentences=[prepare_sentence(x) for x in paragraph['sentences']]
        )
        return [res] if res['sentences'] else []


def prepare_paragraphs(section, findings_section):
    if findings_section is not None:
        section_result = list()
        paragraphs_bundle = dict(hidden=True, paragraphs=list())
        for paragraph_index, paragraph in enumerate(section['paragraphs']):
            findings_paragraph = find_matching_paragraph(paragraph_index, findings_section)
            hidden = True if findings_paragraph is None else False

            if paragraphs_bundle['hidden'] == hidden:
                paragraphs_bundle['paragraphs'].append(prepare_sentences(paragraph, findings_paragraph))
            else:
                if len(paragraphs_bundle['paragraphs']) > 0:
                    section_result.append(paragraphs_bundle)
                paragraphs_bundle = dict(hidden=hidden, paragraphs=[prepare_sentences(paragraph, findings_paragraph)])
        if len(paragraphs_bundle['paragraphs']) > 0:
            section_result.append(paragraphs_bundle)
        return section_result
    else:
        res = dict(
            hidden=False,
            paragraphs=[prepare_sentences(x) for x in section['paragraphs']]
        )
        return [res] if res['paragraphs'] else []


def prepare_sections(article_data):
    result = []
    for section_index, section in enumerate(article_data.text):
        findings_section = find_matching_section(section_index, article_data.findings)

        section_data = {
            'title': section['title'],
            'hidden': True if findings_section is None else False,
            'paragraphs_bundles': prepare_paragraphs(section, findings_section)
        }
        result.append(section_data)

    return result
