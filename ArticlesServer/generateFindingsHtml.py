import logging

class IdAssigner():
    someId = 1
    def getNextId():
        IdAssigner.someId+=1
        return IdAssigner.someId

def sentenceToHtml(sentenceText, foundSentence):
    hiddenSentence = ''
    # if foundSentence is None:
    #     hiddenSentence = 'hidden'

    resultSentenceHtml = '            <span class="sentenceText" '+ hiddenSentence +'>'
    if foundSentence is not None:
        for finding in reversed(foundSentence["findings"]):
          sentenceText = sentenceText[:finding[0]] \
              + "<mark>" \
              + sentenceText[finding[0]:finding[1]] \
              + "</mark>" \
              + sentenceText[finding[1]:]

    resultSentenceHtml+=sentenceText.replace('}', ' ').replace('{', ' ').replace('\\',' ')
    resultSentenceHtml += '</span>\n'

    return resultSentenceHtml



def findMatchingSentence(sentenceIndex, foundParagraph):
    foundSentence = None
    if foundParagraph is not None:
        foundSentences = [x for x in foundParagraph["sentences"] if sentenceIndex == x["sentenceIndex"]]
        if len(foundSentences) > 0:
            foundSentence = foundSentences[0]
    return foundSentence


paragraphHtml = '''
<div>
%s
</div>
'''

expandableSentences = '''
       <span class="paragraphText" id="sentence-%s" hidden>
%s
       </span>
       <button aria-expanded="false" aria-controls="sentence-%s" class="toggle-content">
            <span class="text">...</span></button>
'''


def paragraphToHtml(paragraphText, foundParagraph):
    hiddenParagraph = ''
    hiddenButton = 'hidden'
    if foundParagraph is None:
        hiddenParagraph = 'hidden'
        hiddenButton = str()

    paragraphResult = str()

    sentencesToBeExpanded = str()

    for sentenceIndex in range(len(paragraphText["sentences"])):
        matchingSentence = findMatchingSentence(sentenceIndex, foundParagraph)
        sentenceResult = sentenceToHtml(
            paragraphText["sentences"][sentenceIndex],
            matchingSentence)
        if matchingSentence is None and foundParagraph is not None:
            sentencesToBeExpanded += sentenceResult
        else:
            if sentencesToBeExpanded != str():
                nextId = IdAssigner.getNextId()
                paragraphResult += expandableSentences%(nextId, sentencesToBeExpanded, nextId)
                sentencesToBeExpanded = str()
            paragraphResult += sentenceResult

    if sentencesToBeExpanded != str():
        nextId = IdAssigner.getNextId()
        paragraphResult += expandableSentences%(nextId, sentencesToBeExpanded, nextId)
        sentencesToBeExpanded = str()

    return paragraphHtml%paragraphResult

def findMatchingParagraph(paragraphIndex, foundSection):
    foundParagraph = None
    if foundSection is not None:
        foundParagraphs =  [x for x in foundSection["paragraphs"] if paragraphIndex == x["paragraphIndex"]]
        if len(foundParagraphs) > 0:
            foundParagraph = foundParagraphs[0]
    return foundParagraph



sectionHtml = '''
    <li + %s>
    <div class="collapsible-header">  %s  </div>
    <div class="collapsible-body">
    <span>
%s
    </span></div>
    </li>
'''


expandableParagraph = '''
       <div class="paragraphText" id="paragraph-%s" hidden>
%s
       </div>
       <button aria-expanded="false" aria-controls="paragraph-%s" class="toggle-content">
            <span class="text">Expand</span></button>
'''


def sectionToHtml(sectionText, foundSection):
    hiddenSection = 'class="active"'
    if foundSection is None:
        hiddenSection = str()

    sectionResult = str()

    paragraphsToBeExpanded = str()


    for paragraphIndex in range(len(sectionText["paragraphs"])):
        matchingParagraph = findMatchingParagraph(paragraphIndex, foundSection)
        paragraphResult = paragraphToHtml(
                sectionText["paragraphs"][paragraphIndex],
                matchingParagraph)

        if matchingParagraph is None and foundSection is not None:
            paragraphsToBeExpanded += paragraphResult
        else:
            if paragraphsToBeExpanded != str():
                nextId = IdAssigner.getNextId()
                sectionResult+= expandableParagraph%(nextId, paragraphsToBeExpanded, nextId)
                paragraphsToBeExpanded = str()
            sectionResult+=paragraphResult

    if paragraphsToBeExpanded != str():
        nextId = IdAssigner.getNextId()
        sectionResult+= expandableParagraph%(nextId, paragraphsToBeExpanded, nextId)
        paragraphsToBeExpanded = str()


    return sectionHtml%(hiddenSection, sectionText["title"], sectionResult)


def findMatchingSection(sectionIndex, wholeArticleFindings):
    foundSection = None
    foundSections = [x for x in wholeArticleFindings if sectionIndex == x["sectionIndex"]]
    if len(foundSections) > 0:
        foundSection = foundSections[0]
    return foundSection




navigationAddon = '''
      <ul id="slide-out" class="sidenav">
        <li><div class="user-view">
          <a href="#user"><img class="circle" src="images/yuna.jpg"></a>
          <a href="#name"><span class="white-text name">John Doe</span></a>
          <a href="#email"><span class="white-text email">jdandturk@gmail.com</span></a>
        </div></li>
        <li><a href="#!"><i class="material-icons">cloud</i>First Link With Icon</a></li>
        <li><a href="#!">Second Link</a></li>
        <li><div class="divider"></div></li>
        <li><a class="subheader">Subheader</a></li>
        <li><a class="waves-effect" href="#!">Third Link With Waves</a></li>
      </ul>
      <a href="#" data-target="slide-out" class="sidenav-trigger"><i class="material-icons">menu</i></a>
'''


baseHtml = '''

  <!DOCTYPE html>
  <html>
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
          <ul id="nav-mobile" class="right hide-on-med-and-down">
            <li><a href="{{ url_for("doi.index") }}">Index</a></li>
            <li><a href="{{url_for("doi.prevDoi", doi = "%s")}}">Previous</a></li>
            <li><a href="{{url_for("doi.nextDoi", doi = "%s")}}">Next</a></li>
          </ul>
        </div>
      </nav>


      %s

       %s
      <!--JavaScript at end of body for optimized loading-->

      <script type="text/javascript" src="{{ url_for('static', filename='js/materialize.min.js') }}"></script>

      <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
      <script>
        var elem = document.querySelector('.collapsible.expandable');
        var instance = M.Collapsible.init(elem, {
          accordion: false
        });
      </script>

      <script>
          document.addEventListener('DOMContentLoaded', function() {
            var elems = document.querySelectorAll('.sidenav');
            var instances = M.Sidenav.init(elems, {});
          });
      </script>

    <script>
        if ('querySelector' in document && 'addEventListener' in window) {

            var toggleButtons = document.querySelectorAll('.toggle-content');
            var fullTextWrappers = document.querySelectorAll('.paragraphText');
            var fullText;
            var toggleButtonText;


            [].forEach.call(toggleButtons, function(toggleButton) {
                // add listener for each button

                toggleButton.addEventListener('click', function () {
                    fullTextWrapper = this.parentElement.querySelector('#'+ this.getAttribute('aria-controls'));
                    toggleButtonText = this.querySelector('.text');

                    if (!fullTextWrapper.hasAttribute('hidden')) {
                        toggleButtonText.innerText = 'Show More';
                        fullTextWrapper.setAttribute('hidden', true);
                        toggleButton.setAttribute('aria-expanded', false);
                    } else {
                        fullTextWrapper.removeAttribute('hidden');
                        this.setAttribute('hidden', true);
                    }
                });
            });
        }
    </script>

    </body>
  </html>
'''

titleHtmlBase = '''
    <h3 class="header"> %s </h3>
    <h6> <b> Authors: </b> %s;<emsp><emsp> <b>Publisher</b> %s; <emsp> <b>Doi:</b> %s </h6>
    <h6> Status: %s </h6>
    %s
    <div>
'''

buttonReject = '''
        <a class="waves-effect waves-light btn red" href="{{url_for("doi.reject", doi = "%s")}}">
         Reject</a>
'''
buttonAccept =  '<a class="waves-effect waves-light btn green" href="{{url_for("doi.accept", doi = "%s")}}">Accept</a>'
buttonTodo =  '<a class="waves-effect waves-light btn" href="{{url_for("doi.restore", doi = "%s")}}">Clear</a>'


def getTitlePart(doiFileBasename, articleData):
    authors = ', '.join([a.get("given", str())+' '+a.get("family", str()) for a in articleData["article"]["authors"]])
    doiLink = '<a href="https://doi.org/%s">%s</a>'%(articleData["article"]["doi"], articleData["article"]["doi"])

    buttons = buttonAccept%doiFileBasename +\
      buttonReject%doiFileBasename +\
      buttonTodo%doiFileBasename
    return titleHtmlBase%(
      articleData["article"]["title"],
      authors,
      articleData["article"]["publisher"],
      doiLink,
      articleData["status"],
      buttons)


def generateFindingsHtml(doiFileBasename, articleData):
    result = '<ul class="collapsible expandable">'
    for sectionIndex in range(len(articleData["article"]["text"])):
        result += sectionToHtml(
            articleData["article"]["text"][sectionIndex],
            findMatchingSection(sectionIndex, articleData["findings"]))
    result += '</ul>'

    return baseHtml%( doiFileBasename,doiFileBasename, getTitlePart(doiFileBasename, articleData), result)
