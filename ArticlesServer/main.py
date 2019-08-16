from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, render_template_string
)
import os
import json
import logging
from werkzeug.utils import secure_filename

from .generate_articles_database import generate_articles_database
from extract_doi_from_csv import extract_doi_from_csv
from utilities import load_variable
from .DatabaseManager import DatabaseManager
from .prepare_sections import prepare_sections

main = Blueprint('main', __name__)


@main.route('/')
def index():
    db = DatabaseManager.get_instance()
    if db:
        return render_template('main_with_articles.html',
                               articles_with_findings=[db.get_short_article_info(x) for x in
                                                       db.get_all_valid_with_findings()],
                               articles_without_findings=[db.get_short_article_info(x) for x in
                                                          db.get_all_valid_without_findings()],
                               articles_with_error=[db.get_short_article_info(x) for x in
                                                    db.get_all_invalid_articles()])
    else:
        return render_template('main_without_articles.html')


@main.route('/upload', methods=["GET"])
def upload_view():
    return render_template('upload_view.html')


def get_or_create_upload_path():
    uploadFolder = './serverUploads'
    if not os.path.exists(uploadFolder):
        os.makedirs(uploadFolder)
    return uploadFolder


def read_file_from_request(files, name):
    logger = logging.getLogger('read_file_from_request_' + name)
    if name not in files:
        logger.error('No doi list in request')
        return None
    file = files[name]
    if not file or file.filename == str():
        logger.error('No filename given')
        return None
    filename = secure_filename(file.filename)
    filePath = os.path.join(get_or_create_upload_path(), filename)
    file.save(filePath)
    return filePath


def get_doi_list(files):
    filename = read_file_from_request(files, 'doiList')
    if filename:
        return extract_doi_from_csv(filename)
    else:
        return None


def get_finder(files):
    filename = read_file_from_request(files, 'finder')
    if filename:
        return load_variable(filename, 'finder')
    else:
        return None


@main.route('/upload', methods=["POST"])
def upload_post():
    logger = logging.getLogger('upload_post')
    doiList = get_doi_list(request.files)
    if doiList is None:
        logger.error('Wrong doi list provided')
        flash("Invalid doi list")
        return redirect(url_for("main.upload_view"))
    finder = get_finder(request.files)
    if finder is None:
        logger.error('Wrong finder provided')
        flash("Invalid finder")
        return redirect(url_for("main.upload_view"))
    logger.info('Properly read doiList and finder, doi list size is ' + str(len(doiList)))

    DatabaseManager.reload_database(doiList, finder)
    return redirect(url_for('main.index'))




def generate_data_doi_data(doi_id, article_with_findings):
    return {
        'doi_id': doi_id,
        'title': article_with_findings['article']['title'],
        'doi': article_with_findings['article']['doi'],
        'publisher': article_with_findings['article']['doi'],
        'authors': article_with_findings['article']['authors'],
        'sections': prepare_sections(article_with_findings)}


@main.route('/doiView/<string:doi_id>')
def view_doi(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))
    article_with_findings = db.get_full_article(doi_id)

    return render_template(
        "doi_view.html",
        display_data=generate_data_doi_data(doi_id, article_with_findings))

@main.route('/api/doiView/<string:doi_id>')
def api_doi(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))
    article_with_findings = db.get_full_article(doi_id)

    return json.dumps(generate_data_doi_data(doi_id, article_with_findings))

@main.route('/next/<string:doi_id>')
def next_doi(doi_id):
    db = DatabaseManager.get_instance()
    next = db.get_next_article(doi_id)
    if next:
        return redirect(url_for('main.view_doi', doi_id=next))
    else:
        return redirect(url_for('main.index'))


@main.route('/prev/<string:doi_id>')
def prev_doi(doi_id):
    db = DatabaseManager.get_instance()
    prev = db.get_prev_article(doi_id)
    if prev:
        return redirect(url_for('main.view_doi', doi_id=prev))
    else:
        return redirect(url_for('main.index'))

