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


STATUS_ACCEPTED  = '<a class="waves-light btn-small green">Accepted</a>'
STATUS_TO_DO = '<a class="waves-light btn-small yellow">To be checked</a>'
STATUS_REJECTED = '<a class="waves-light btn-small red">Rejected</a>'

#STATUS_ACCEPTED = '<font color="green">Accepted</font>'
#STATUS_REJECTED = '<font color="red">Rejected</font>'
#STATUS_TO_DO    = '<font color="yellow">To be checked</font>'

def prepareArticles(finderResultsFolder, articlesJsons):
    result = dict()
    for articleFilename in os.listdir(articlesJsons):
        articleFullPath = articlesJsons+"/"+articleFilename
        foundFullPath = finderResultsFolder + "/" + articleFilename

        with open(articleFullPath, 'r') as articleFile:
            foundArticle = json.load(articleFile)

            if os.path.isfile(foundFullPath):
                with open(foundFullPath, 'r') as foundFile:
                    foundData = json.load(foundFile)
                    result[articleFilename.replace('.json', '')] = dict(
                      article = foundArticle,
                      findings = foundData,
                      status = STATUS_TO_DO)
            #Uncomment for articles without findings
            # else:
            #     result[articleFilename.replace('.json', '')] = {"article" : foundArticle, "findings" : []}
    return result

articles = prepareArticles('outputFinder', 'outputArticles')



bp = Blueprint('doi', __name__, url_prefix='/doi')


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

@bp.route('/index')
def index():
    articlesWithFindings = ''
    articlesWithoutFindings = ''

    for doiName, value in articles.items():
        doiRepresentation = '<li  class="collection-item"><a class="action" href="{{ url_for("doi.doi", doi="' \
         + doiName +'") }}">'+ value['article']['title'] +'</a><br> Status: ' + value["status"] + '</li>'
        if len(value['findings']) > 0:
            articlesWithFindings+=doiRepresentation
        else:
            articlesWithoutFindings+=doiRepresentation

    return render_template_string(baseIndex%(articlesWithFindings, articlesWithoutFindings))




@bp.route('/<string:doi>', methods=('GET', 'POST'))
def doi(doi):
    return render_template_string(generateFindingsHtml(doi, articles[doi]))
    return generateFindingsHtml(doi, articles[doi]["article"], articles[doi]["findings"])



@bp.route('/next/<string:doi>', methods=('GET', 'POST'))
def nextDoi(doi):
    print("finding for " + doi)

    articleKeys = list(articles.keys())
    nextDoiIter = articleKeys.index(doi) + 1

    if len(articleKeys) > nextDoiIter:
        return redirect(url_for('doi.doi', doi=articleKeys[nextDoiIter]))
    else:
        return redirect(url_for('doi.index'))



@bp.route('/prev/<string:doi>', methods=('GET', 'POST'))
def prevDoi(doi):
    print("finding for " + doi)

    articleKeys = list(articles.keys())
    prevDoiIter = articleKeys.index(doi) - 1

    if prevDoiIter > 0:
        return redirect(url_for('doi.doi', doi=articleKeys[prevDoiIter]))
    else:
        return redirect(url_for('doi.index'))




@bp.route('/accept/<string:doi>', methods=('GET', 'POST'))
def accept(doi):
  articles[doi]["status"] = STATUS_ACCEPTED
  return redirect(url_for('doi.doi', doi=doi))

@bp.route('/reject/<string:doi>', methods=('GET', 'POST'))
def reject(doi):
  articles[doi]["status"] = STATUS_REJECTED
  return redirect(url_for('doi.doi', doi=doi))


@bp.route('/restore/<string:doi>', methods=('GET', 'POST'))
def restore(doi):
  articles[doi]["status"] = STATUS_TO_DO
  return redirect(url_for('doi.doi', doi=doi))