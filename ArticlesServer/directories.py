import os

BASE_DIRECTORY = os.getcwd() + '/.server_files'
OUTPUT_DB = BASE_DIRECTORY + '/' +'comments_and_statuses'
OUTPUT_DIRECTORY = BASE_DIRECTORY + '/' + 'articles'
USERS_FILE = BASE_DIRECTORY + '/users.json'
DOIS_FILE = BASE_DIRECTORY + '/dois.csv'

DOIS_TEMP = BASE_DIRECTORY + '/dois_temp.csv'
FINDER_TEMP = BASE_DIRECTORY + '/finder_temp.txt'

INPUT_FILES_DIRECTORY = BASE_DIRECTORY + '/InputFiles'
FINDER_FILE = INPUT_FILES_DIRECTORY + '/finder.txt'

from ArticlesDataDownloader.InputSourceType import InputSourceType

PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES = [
    ('IEEE CSV', INPUT_FILES_DIRECTORY + '/IEEE', InputSourceType.IEEE_CSV),
    ('Science direct RIS', INPUT_FILES_DIRECTORY + '/Science_direct', InputSourceType.SCIENCE_DIRECT_RIS),
    ('Springer CSV', INPUT_FILES_DIRECTORY + '/Springer', InputSourceType.SPRINGER_CSV),
    ('Willey RIS', INPUT_FILES_DIRECTORY + '/Willey', InputSourceType.WILLEY_RIS),
    ('ACM BIB', INPUT_FILES_DIRECTORY + '/ACM', InputSourceType.ACM_BIB),
    ('Scopus CSV', INPUT_FILES_DIRECTORY + '/Scopus', InputSourceType.SCOPUS_CSV),
]
