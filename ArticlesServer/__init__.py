import os

from flask import Flask
from flask_jsglue import JSGlue
from requests import Session

from TextSearchEngine.parse_finder import parse_finder
from AutomatedSearchHelperUtilities.configuration import configureLogger
from AutomatedSearchHelperUtilities.extract_doi_from_csv import extract_doi_from_csv
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
from .directories import BASE_DIRECTORY, DOIS_FILE, FINDER_FILE, INPUT_FILES_DIRECTORY, PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES

ALLOWED_EXTENSIONS = {'csv'}


def create_app(test_config=None):

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print ('creating dir ' + BASE_DIRECTORY)
        createDirectoryIfNotExists(BASE_DIRECTORY)
        createDirectoryIfNotExists(INPUT_FILES_DIRECTORY)
        for _, directory, _ in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES:
            createDirectoryIfNotExists(directory)
        configureLogger()
        try:
            from ArticlesServer.database.DatabaseManager import DatabaseManager
            print('Database reload start')
            DatabaseManager.reload_database()
            print('Successfully reloaded articles')
        except Exception as e:
            print(e)
            print("Could not load old configuration")

    app = Flask(__name__, instance_relative_config=True)
    jsglue = JSGlue(app)

    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    sess = Session()

    from .main import main
    app.register_blueprint(main)

    return app
