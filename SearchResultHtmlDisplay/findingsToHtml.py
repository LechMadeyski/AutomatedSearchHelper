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

    resultSentenceHtml+=sentenceText
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





baseHtml = '''

  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="UTF-8">
      <!--Import Google Icon Font-->
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <!--Import materialize.css-->
      <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>

      <!--Let browser know website is optimized for mobile-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>

%s
    </div>
    <body>
       %s
      <!--JavaScript at end of body for optimized loading-->
      <script type="text/javascript" src="js/materialize.min.js"></script>
      <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

      <script>
        var elem = document.querySelector('.collapsible.expandable');
        var instance = M.Collapsible.init(elem, {
          accordion: false
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
    <div>
'''

def getTitlePart(articleData):
    authors = ', '.join(articleData["authors"])
    doiLink = '<a href="https://doi.org/%s">%s</a>'%(articleData["doi"], articleData["doi"])
    return titleHtmlBase%(articleData["title"], authors, articleData["publisher"], doiLink)

def findingsToHtml(articleData, wholeArticleFindings):
    result = '<ul class="collapsible expandable">'
    for sectionIndex in range(len(articleData["text"])):
        result += sectionToHtml(
            articleData["text"][sectionIndex],
            findMatchingSection(sectionIndex, wholeArticleFindings))
    result += '</ul>'
    return baseHtml%(getTitlePart(articleData), result)
