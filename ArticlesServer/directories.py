import os

BASE_DIRECTORY = os.path.join(os.getcwd(), '.server_files')
OUTPUT_DB = os.path.join(BASE_DIRECTORY, 'comments_and_statuses')
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, 'articles')
USERS_FILE = os.path.join(BASE_DIRECTORY, 'users.json')
DOIS_FILE = os.path.join(BASE_DIRECTORY, 'dois.csv')

DOIS_TEMP = os.path.join(BASE_DIRECTORY, 'dois_temp.csv')
FINDER_TEMP = os.path.join(BASE_DIRECTORY, 'finder_temp.txt')

INPUT_FILES_DIRECTORY = os.path.join(BASE_DIRECTORY, 'InputFiles')
FINDER_FILE = os.path.join(BASE_DIRECTORY, 'finder.txt')

from ArticlesDataDownloader.InputSourceType import InputSourceType

PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES = [
    ('IEEE CSV', os.path.join(INPUT_FILES_DIRECTORY, 'IEEE'), InputSourceType.IEEE_CSV),
    ('Science direct RIS', os.path.join(INPUT_FILES_DIRECTORY, 'Science_direct'), InputSourceType.SCIENCE_DIRECT_RIS),
    ('Springer CSV', os.path.join(INPUT_FILES_DIRECTORY, 'Springer'), InputSourceType.SPRINGER_CSV),
    ('Willey RIS', os.path.join(INPUT_FILES_DIRECTORY, 'Willey'), InputSourceType.WILLEY_RIS),
    ('ACM BIB', os.path.join(INPUT_FILES_DIRECTORY, 'ACM'), InputSourceType.ACM_BIB),
    ('Scopus CSV', os.path.join(INPUT_FILES_DIRECTORY, 'Scopus'), InputSourceType.SCOPUS_CSV),
]
