import csv


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
                    if index < len(row_names):
                        entry[row_names[index]] = value.strip()
                result.append(entry)
    return result
