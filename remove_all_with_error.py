import os
import json
from collections import defaultdict
from random import randint

BASE_DIR = os.path.join('.server_files', 'articles')
filenames_per_status = defaultdict(list)
filenames_with_pdf_read = list()
filenames_with_pdf_read_with_multiple_sections = list()


filenames_to_change_read = list()
for filename in [BASE_DIR + '/' + f for f in os.listdir(BASE_DIR) if f[-5:] == '.json']:
    with open(filename) as filestream:
        article_dict = json.load(filestream) or dict()
        status = article_dict.get('read_status', str())
        filenames_per_status[status].append(filename)


for status, filenames in filenames_per_status.items():
    print('Status <' + status + '> filenames size: ' + str(len(filenames)))
    if status == "XXXX":
        for filename in filenames:
            pdf_filename = filename.replace('.json', '.pdf')
            if os.path.isfile(pdf_filename):
                os.remove(pdf_filename)
            os.remove(filename)

