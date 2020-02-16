import slate as slate

from nltk import tokenize

def formatTextAndSplitIntoSentences(text):
    return [s for s in tokenize.sent_tokenize(text.replace("\n", "").replace("\r", "")) if len(s)>0]


def read_pdf_as_json(filename):
    with open(filename, 'rb') as f:
        extracted_text = slate.PDF(f)
    split_text = []

    for extracted_part in extracted_text:
        split_text += extracted_part.replace('\\n', '\n').split('\n')

    sections = []
    current_section = dict(title='Begining data', text=str())
    prev = str()
    for part in split_text:
        if (part.isupper() and prev.isnumeric()) or part == 'REFERENCES' or part == 'ABSTRACT':
            sections.append(dict(
                title=current_section['title'],
                paragraphs=[dict(sentences=formatTextAndSplitIntoSentences(current_section['text']))]))
            current_section = dict(title=part, text=str())
        else:
            if part.endswith('-'):
                current_section['text'] += part[:-1]
            else:
                current_section['text'] += part + ' '
        prev = part

    if current_section['text']:
        sections.append(dict(
            title=current_section['title'],
            paragraphs=[dict(sentences=formatTextAndSplitIntoSentences(current_section['text']))]))
    return sections
