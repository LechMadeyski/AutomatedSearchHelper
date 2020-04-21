import csv
from ArticlesDataDownloader.format_text_and_split_into_sentences import format_text_and_split_into_sentences

def read_csv_as_dicts(filepath):
    result = list()
    with open(filepath, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_names = []
        for line_no, row in enumerate(csv_reader):
            if line_no == 0:
                row_names = [x for x in row]
            else:
                entry = dict()
                for index, value in enumerate(row):
                    entry[row_names[index]] = value
                result.append(entry)
        print(row_names)

    return result


def create_abstract(text):
    if text:
        return [dict(title='Abstract', paragraphs=[dict(sentences=format_text_and_split_into_sentences(text))])]
    else:
        return str()
