import os
import json
from collections import defaultdict
from random import randint

BASE_DIR = os.path.join('.server_files', 'articles')
filenames_per_status = defaultdict(list)
filenames_with_pdf_read = list()
filenames_with_pdf_read_with_multiple_sections = list()
acm_published = list()


filenames_to_change_read = list()
for filename in [BASE_DIR + '/' + f for f in os.listdir(BASE_DIR) if f[-5:] == '.json']:
    with open(filename) as filestream:
        article_dict = json.load(filestream) or dict()
        status = article_dict.get('read_status', str())
        filenames_per_status[status].append(filename)
        if  article_dict.get('publisher_link', str()) and 'acm.org' in article_dict.get('publisher_link', str()):
            acm_published.append(filename)
        for section in article_dict.get('text', list()):
            if section['title'] == 'Begining data':
                filenames_with_pdf_read.append(filename)
                if len(article_dict.get('text', list())) > 2:
                    filenames_with_pdf_read_with_multiple_sections.append(filename)


i=0
for status, filenames in filenames_per_status.items():
    print('Status <' + status + '> filenames size: ' + str(len(filenames)))
    if status == 'OK - PDF READ' or status == 'Failed reading pdf data':
       for fname in filenames:
            os.remove(fname)
            pdf_filename = fname.replace('.json', '.pdf')
            if os.path.isfile(pdf_filename):
                os.remove(pdf_filename)
print('No of failed acm' + str(i))
print('Filenames with reading from : ' + str(len(filenames_with_pdf_read)))
print('Filenames with mutliple sections : ' + str(len(filenames_with_pdf_read_with_multiple_sections)))

print('No of acm type ' + str(len(acm_published)))


