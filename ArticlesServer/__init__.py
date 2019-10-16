import os

from flask import Flask
from requests import Session

from TextSearchEngine.parse_finder import parse_finder
from configuration import configureLogger
from extract_doi_from_csv import extract_doi_from_csv
from utilities import createDirectoryIfNotExists, load_variable
from .directories import BASE_DIRECTORY, DOIS_FILE, FINDER_FILE

ALLOWED_EXTENSIONS = {'csv'}


def create_app(test_config=None):
    createDirectoryIfNotExists(BASE_DIRECTORY)
    configureLogger()
    app = Flask(__name__, instance_relative_config=True)

    try:
        doi_list = extract_doi_from_csv(DOIS_FILE)
        with open(FINDER_FILE, 'r') as finder_file:
            finder = parse_finder(finder_file.read())
        from ArticlesServer.database.DatabaseManager import DatabaseManager
        DatabaseManager.reload_database(doi_list, finder)
    except:
        print("Could not load old configuration")

    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    sess = Session()

    from .main import main
    app.register_blueprint(main)

    return app
