import os

from flask import Flask
from requests import Session

from configuration import configureLogger

ALLOWED_EXTENSIONS = {'csv'}


def create_app(test_config=None):
    configureLogger()
    app = Flask(__name__, instance_relative_config=True)


    # if test_config is None:
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)
    #
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    sess = Session()

    from .main import main
    app.register_blueprint(main)

    from .doi import doi
    app.register_blueprint(doi)
#    app.add_url_rule('/doi', endpoint='index')


    return app