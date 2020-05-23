from nltk import tokenize


def format_text_and_split_into_sentences(text):
    return tokenize.sent_tokenize(text.replace("\n", "").replace("\r", ""))


def create_abstract(text):
    if text:
        return [dict(title='Abstract', paragraphs=[dict(sentences=format_text_and_split_into_sentences(text))])]
    else:
        return list()
