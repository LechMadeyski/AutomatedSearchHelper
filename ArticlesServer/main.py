from flask import (
    Blueprint, flash, redirect, render_template, url_for, request, session
)
import os
import json
import logging
from werkzeug.utils import secure_filename

from extract_doi_from_csv import extract_doi_from_csv
from utilities import load_variable
from ArticlesServer.database.DatabaseManager import DatabaseManager
from .prepare_sections import prepare_sections
from TextSearchEngine.parse_finder import parse_finder
from .database.Status import Status
from .database.UsersDatabase import get_user_database
from .directories import DOIS_FILE, FINDER_FILE

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, validators

main = Blueprint('main', __name__)


@main.route('/')
def index():
    db = DatabaseManager.get_instance()

    user = None
    if session.get('user', None):
        user = session['user']['login']

    if db:
        return render_template('main_with_articles.html',
                               articles_with_findings=[db.get_short_article_info(x, user) for x in
                                                       db.get_all_valid_with_findings()],
                               articles_without_findings=[db.get_short_article_info(x, user) for x in
                                                          db.get_all_valid_without_findings()],
                               articles_with_error=[db.get_short_article_info(x, user) for x in
                                                    db.get_all_invalid_articles()])
    else:
        return render_template('main_without_articles.html')


def get_or_create_upload_path():
    uploadFolder = './serverUploads'
    if not os.path.exists(uploadFolder):
        os.makedirs(uploadFolder)
    return uploadFolder


def get_doi_list(doi_list_form):
    filename = doi_list_form and doi_list_form.data and doi_list_form.data.filename
    if filename:
        return extract_doi_from_csv(filename)
    else:
        return None


def get_finder_string_from_file(finder_form):
    filename = finder_form and finder_form.data and finder_form.data.filename
    if filename:
        try:
            with open(filename, 'r') as finder_file:
                return finder_file.read()
        except:
            flash('Could not open file '+ str(filename))
            return None
    else:
        return None


class UploadForm(FlaskForm):
    doi_list = FileField('doi_list', validators=[
        FileRequired()
    ])
    finder = FileField('finder')
    finder_text = StringField('finder_text')


@main.route('/upload', methods=["GET", "POST"])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        logger = logging.getLogger('upload_post')
        doiList = get_doi_list(form.doi_list)
        if doiList is None:
            logger.error('Wrong doi list provided')
            flash("Invalid doi list")
            return render_template('upload_view.html', form=form)
        finder_text = get_finder_string_from_file(form.finder)
        finder = None
        if finder_text is None:
            finder_text = str(form.finder_text.data)
        try:
            logger.info("Parsing finder from : " + finder_text)
            finder = parse_finder(finder_text)
        except ValueError as e:
            flash("Invalid finder text " + str(e))

        if finder is None:
            logger.error('Wrong finder provided')
            return render_template('upload_view.html', form=form)
        logger.info('Properly read doiList and finder, doi list size is ' + str(len(doiList)))

        form.doi_list.data.save(DOIS_FILE)

        with open(FINDER_FILE, 'w') as finder_file:
            finder_file.write(str(finder))

        DatabaseManager.reload_database(doiList, finder)
        return redirect(url_for('main.index'))

    return render_template('upload_view.html', form=form)


def can_remove_comment(login):
    user = session['user']
    if user:
        return user['login'] == login
    else:
        return False

def prepare_comments(db, doi_id):
    return [
        dict(text=c['text'],
             comment_id=c['comment_id'],
             user_name=get_user_database().get_full_name(c['user']),
             can_delete=can_remove_comment(c['user'])) for c in db.get_comments(doi_id)]


def prepare_statuses(db, doi_id):
    if session.get('user', None):
        return db.get_statuses(doi_id, session['user']['login'])
    return db.get_statuses(doi_id)


def generate_data_doi_data(db, doi_id):
    article_with_findings = db.get_full_article(doi_id)
    return {
        'doi_id': doi_id,
        'comments': prepare_comments(db, doi_id),
        'statuses': prepare_statuses(db, doi_id),
        'title': article_with_findings['article']['title'],
        'doi': article_with_findings['article']['doi'],
        'issn': article_with_findings['article']['issn'],
        'published_in' : article_with_findings['article']['journalName'],
        'jurnal_info': article_with_findings['article']['journalInfo'],
        'publisher': article_with_findings['article']['publisher'],
        'authors': article_with_findings['article']['authors'],
        'sections': prepare_sections(article_with_findings)}


class CommentForm(FlaskForm):
    comment = StringField('comment')


@main.route('/doiView/<string:doi_id>', methods=['GET', 'POST'])
def view_doi(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not session['user']:
            flash("Please login to comment articles")
        else:
            db.add_comment(doi_id, str(comment_form.comment.data), session['user']['login'])

    comment_form.comment.data = str()

    return render_template(
        "doi_view.html",
        display_data=generate_data_doi_data(db, doi_id),
        comment_form=comment_form)


@main.route('/removeComment/<string:doi_id>')
def remove_comment(doi_id):
    db = DatabaseManager.get_instance()
    db.remove_comment(doi_id, int(request.args.get('comment_id')))
    return redirect(url_for('main.view_doi', doi_id=doi_id))


@main.route('/api/doiView/<string:doi_id>')
def api_doi(doi_id):
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))
    return json.dumps(generate_data_doi_data(db, doi_id))


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


@main.route('/status/<string:doi_id>')
def change_status(doi_id):
    status = request.args.get('status')
    db = DatabaseManager.get_instance()
    if not db:
        return redirect(url_for('main.index'))

    user = session['user']

    if not user:
        flash('Cannot change status without being logged in')
        return redirect(url_for('main.login'))

    if status == '1':
        db.change_status(doi_id, user['login'], Status.TO_BE_CHECKED)
    elif status == '2':
        db.change_status(doi_id, user['login'],  Status.ACCEPTED)
    elif status == '3':
        db.change_status(doi_id, user['login'],  Status.DECLINED)

    return redirect(url_for('main.view_doi', doi_id=doi_id))


class LoginForm(FlaskForm):
    login = StringField('login')
    password = PasswordField('password')


@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = get_user_database().login(login_form.login.data, login_form.password.data)
        if user:
            session['user'] = user
            return redirect(url_for('main.index'))
        else:
            flash('Incorrect credentials')

    return render_template('login.html', form=login_form)


@main.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for('main.index'))


class RegisterForm(FlaskForm):
    login = StringField('Login')
    full_name = StringField('Name')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@main.route('/register', methods = ["GET", "POST"])
def register():
    if session.get('user', None):
        flash('Please logout if you want to register')
        return redirect(url_for('main.index'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        register_success = get_user_database().register(register_form.login.data,
                                                        register_form.full_name.data,
                                                        register_form.password.data)
        if register_success:
            flash("Successfully registered new user, please log in")
            return redirect(url_for('main.login'))
        else:
            flash("This login is occupied")

    return render_template('register.html', form=register_form)
