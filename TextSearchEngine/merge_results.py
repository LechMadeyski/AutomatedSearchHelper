from copy import deepcopy
from TextSearchEngine.merge_findings import merge_findings


def merge_sentences(finalResultSentence, sentenceToBeMerged):
    finalResultSentence["findings"] = merge_findings(finalResultSentence["findings"] + sentenceToBeMerged["findings"])


def merge_paragraphs(finalResultParagraph, paragraphToBeMerged):
    for sentenceToBeMerged in paragraphToBeMerged["sentences"]:
        matchingSentence = [x for x in finalResultParagraph["sentences"] if
                            sentenceToBeMerged["sentenceIndex"] == x["sentenceIndex"]]
        if matchingSentence:
            merge_sentences(matchingSentence[0], sentenceToBeMerged)
        else:
            finalResultParagraph["sentences"].append(deepcopy(sentenceToBeMerged))
    finalResultParagraph["sentences"].sort(key=lambda x: x['sentenceIndex'])


def merge_sections(final_result_section, section_to_be_merged):
    for paragraph_to_be_merged in section_to_be_merged["paragraphs"]:
        matching_paragraph = [x for x in final_result_section["paragraphs"] if
                              paragraph_to_be_merged["paragraphIndex"] == x["paragraphIndex"]]
        if matching_paragraph:
            merge_paragraphs(matching_paragraph[0], paragraph_to_be_merged)
        else:
            final_result_section["paragraphs"].append(deepcopy(paragraph_to_be_merged))
    final_result_section["paragraphs"].sort(key=lambda x: x['paragraphIndex'])


def merge_results(items):
    final_result = None
    for item in items:
        if final_result is None:
            final_result = deepcopy(item)
            continue
        for section_to_be_merged in item:
            matching_section = [x for x in final_result if section_to_be_merged["sectionIndex"] == x["sectionIndex"]]
            if matching_section:
                merge_sections(matching_section[0], section_to_be_merged)
            else:
                final_result.append(deepcopy(section_to_be_merged))
        final_result.sort(key=lambda x: x["sectionIndex"])
    return final_result
