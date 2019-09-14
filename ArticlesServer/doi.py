import functools
import json
import itertools
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template_string
from ArticlesServer.generateFindingsHtml import generateFindingsHtml

import os

STATUS_ACCEPTED = '<a class="waves-light btn-small green">Accepted</a>'
STATUS_TO_DO = '<a class="waves-light btn-small yellow">To be checked</a>'
STATUS_REJECTED = '<a class="waves-light btn-small red">Rejected</a>'


# STATUS_ACCEPTED = '<font color="green">Accepted</font>'
# STATUS_REJECTED = '<font color="red">Rejected</font>'
# STATUS_TO_DO    = '<font color="yellow">To be checked</font>'

def prepareArticles(finderResultsFolder, articlesJsons):
    result = dict()
    if not os.path.isdir(finderResultsFolder) or not os.path.isdir(articlesJsons):
        return result

    for articleFilename in os.listdir(articlesJsons):
        articleFullPath = articlesJsons + "/" + articleFilename
        foundFullPath = finderResultsFolder + "/" + articleFilename

        with open(articleFullPath, 'r') as articleFile:
            foundArticle = json.load(articleFile)

            if os.path.isfile(foundFullPath):
                with open(foundFullPath, 'r') as foundFile:
                    foundData = json.load(foundFile)
                    result[articleFilename.replace('.json', '')] = dict(
                        article=foundArticle,
                        findings=foundData,
                        status=STATUS_TO_DO)
            # Uncomment for articles without findings
            # else:
            #     result[articleFilename.replace('.json', '')] = {"article" : foundArticle, "findings" : []}
    return result


OUTPUT_FINDER_DIRECTORY = 'outputFinder'
OUTPUT_ARTICLES_DIRECTORY = 'outputArticles'


class Articles:
    articles = prepareArticles(OUTPUT_FINDER_DIRECTORY, OUTPUT_ARTICLES_DIRECTORY)
    @staticmethod
    def get_articles():
        return Articles.articles

    @staticmethod
    def set_articles(articles):
        Articles.articles = articles


doi = Blueprint('doi', __name__, url_prefix='/doi')

baseIndex = '''
  <!DOCTYPE html>

    <head>
      <meta charset="UTF-8">
      <!--Import Google Icon Font-->
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">


      <!--Import materialize.css-->
      <link rel="stylesheet" type="text/css" media="screen,projection" href="{{ url_for('static', filename='css/materialize.min.css') }}">


      <!--Let browser know website is optimized for mobile-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>

    <body>

      <nav>
        <div class="nav-wrapper">
          <div class="brand-logo">Automated Search Helper</div>
        </div>
      </nav>

    <h4> </h4>

     <ul class="collection with-header">
      <li class="collection-header"><h4>Articles with findings:</h4></li>
    %s
    </ul>


     <ul class="collection with-header">
      <li class="collection-header"><h4>Articles wihout findings:</h4></li>
    %s
    </ul>

    </body>
  </html>
'''


@doi.route('/')
def index():
    articlesWithFindings = ''
    articlesWithoutFindings = ''

    for doiName, value in Articles.get_articles().items():
        doiRepresentation = '<li  class="collection-item"><a class="action" href="{{ url_for("doi.singleDoi", doi="' \
                            + doiName + '") }}">' + value['article']['title'] + '</a><br> Status: ' + value[
                                "status"] + '</li>'
        if len(value['findings']) > 0:
            articlesWithFindings += doiRepresentation
        else:
            articlesWithoutFindings += doiRepresentation

    return render_template_string(baseIndex % (articlesWithFindings, articlesWithoutFindings))


@doi.route('/<string:doi>', methods=('GET', 'POST'))
def singleDoi(doi):
    return render_template_string(generateFindingsHtml(doi, Articles.get_articles()[doi]))
    # return generateFindingsHtml(doi, Articles.get_articles()[doi]["article"], Articles.get_articles()[doi]["findings"])


@doi.route('/next/<string:doi>', methods=('GET', 'POST'))
def nextDoi(doi):
    print("finding for " + doi)

    articleKeys = list(Articles.get_articles().keys())
    nextDoiIter = articleKeys.index(doi) + 1

    if len(articleKeys) > nextDoiIter:
        return redirect(url_for('doi.singleDoi', doi=articleKeys[nextDoiIter]))
    else:
        return redirect(url_for('doi.index'))


@doi.route('/prev/<string:doi>', methods=('GET', 'POST'))
def prevDoi(doi):
    print("finding for " + doi)

    articleKeys = list(Articles.get_articles().keys())
    prevDoiIter = articleKeys.index(doi) - 1

    if prevDoiIter > 0:
        return redirect(url_for('doi.singleDoi', doi=articleKeys[prevDoiIter]))
    else:
        return redirect(url_for('doi.index'))


@doi.route('/accept/<string:doi>', methods=('GET', 'POST'))
def accept(doi):
    Articles.get_articles()[doi]["status"] = STATUS_ACCEPTED
    return redirect(url_for('doi.singleDoi', doi=doi))


@doi.route('/reject/<string:doi>', methods=('GET', 'POST'))
def reject(doi):
    Articles.get_articles()[doi]["status"] = STATUS_REJECTED
    return redirect(url_for('doi.singleDoi', doi=doi))


@doi.route('/restore/<string:doi>', methods=('GET', 'POST'))
def restore(doi):
    Articles.get_articles()[doi]["status"] = STATUS_TO_DO
    return redirect(url_for('doi.singleDoi', doi=doi))


from run_whole_search import run_whole_search
from utilities import *
from extract_doi_from_csv import extract_doi_from_csv

@doi.route('/regenerate', methods=('GET', 'POST'))
def regenerate():
    doi_list = load_function('doiList.py', 'doiList')()
    finder = load_variable('finder.py', 'finder')
    run_whole_search(doi_list, finder, OUTPUT_ARTICLES_DIRECTORY, OUTPUT_FINDER_DIRECTORY, None,
                     'proxy_auth_plugin.zip')
    Articles.set_articles(prepareArticles(OUTPUT_FINDER_DIRECTORY, OUTPUT_ARTICLES_DIRECTORY))
    return redirect(url_for('doi.index'))








from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['.csv']


@doi.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)

            file.save(os.path.join('uploadedFiles', filename))

            doi_list = extract_doi_from_csv(os.path.join('uploadedFiles', filename))

            finder = load_variable('finder.py', 'finder')
            run_whole_search(doi_list, finder, OUTPUT_ARTICLES_DIRECTORY, OUTPUT_FINDER_DIRECTORY, None,
                             'proxy_auth_plugin.zip')
            Articles.set_articles(prepareArticles(OUTPUT_FINDER_DIRECTORY, OUTPUT_ARTICLES_DIRECTORY))
            return redirect(url_for('doi.index'))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
