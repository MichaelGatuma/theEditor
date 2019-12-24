import traceback
import cfscrape
from bs4 import BeautifulSoup
import sys
import dbmanager

# create anti-cloudflare scraping object
scraper = cfscrape.create_scraper()

##constants
DEVELOPMENT = False;  # Debug Mode
# the home url of the website
baseUrl = ((lambda: 'https://www.homeworkmarket.com', lambda: 'https://www.hwmarket.com:4433')[DEVELOPMENT]())
# a list to store questions
global questions
questions = []
attachments = []
# ha page number
global pageIndex, errorCount, questionIndex
pageIndex=2

def downloadAttachments(links):
    return


def scrapQuestion(url, question):
    global questionIndex
    questionIndex += 1
    try:
        # TODO Display url of a question
        print('>>>', url)
        # get and assign the page containing the question to a variable
        questionPage = scraper.get(url).content
        # parse with BeautifulSoup and get the question div tag
        content = BeautifulSoup(questionPage, 'html.parser').find('div', attrs={'class': 'question'})
        # get the question-body div tag and assign to a variable
        questionBody = content.find('div', attrs={'class': 'question-body'})
        # TODO Display the content of the question
        question['content'] = str(questionBody)
        #print('  ~ Content: ', ((lambda:"NULL", lambda:"OK")[len(questionBody)>0]))
        print('  ~ Content: ', questionBody)
        # get the attachment-list ul tag
        attachmentlist = content.find('ul', attrs={'class': 'attachment-list'})
        # get all the li tags and assign to a variable
        attachmentLinks = attachmentlist.findAll('li')

        # TODO Fetch attachments details
        print('  ~ Attachments:',)
        attachment = {}
        for attachmentLink in attachmentLinks:
            attachment['name'] = attachmentLink.text
            print(attachmentLink.text,)
            attachment['url'] = baseUrl + attachmentLink.a['href'].replace('..', '')
            print('<', baseUrl + attachmentLink.a['href'].replace('..', '', 1),'>;',)
            attachments.append(attachment)
        questionMeta = content.find('div', attrs={'class': 'meta question-meta'})
        print()

        # process each meta separately
        # TODO Display meta information
        print('  ~ Meta:',)
        for meta in questionMeta.findAll('li'):

            # Posted:
            if 'Posted' in str(meta):
                postedAt = meta.text
                postedAt = postedAt.replace('Posted:', '')
                question['posted_at'] = postedAt
                print('Posted:' + postedAt,',',)
            else:
                question['posted_at'] = 'NA'

            # Due:
            if 'Due' in str(meta):
                dueOn = meta.text
                dueOn = dueOn.replace('Due:', '')
                question['due_on'] = dueOn
                print('Due:' + dueOn,',',)
            else:
                question['due_on'] = 'NA'

            # Budget:
            if 'Budget' in str(meta):
                budget = meta.text
                budget = budget.replace('Budget:', '')
                question['budget'] = budget
                print('Budget:' + budget,',',)
            else:
                question['budget'] = 'NA'
        print()
        print()

        # TODO Add each question to a questions object
        questions.append(question)
        if (dbmanager.addQuestion(question, attachments, "null")):
            dbmanager.log(getFootprint(pageIndex, questionIndex))
    except Exception as e:
        # errorCount+=1
        # print('Error',errorCount,'\n'+traceback.format_exc())
        # TODO Handle mid-question Exception
        print('\n! >>> Skipping Question: ', question['title'])
        print(traceback.format_exc())
        pass
    return


def getPageAt(index):
    global questionIndex
    questionIndex = 0
    # append page index to homework answers page url
    pageUrl = baseUrl + '/homework-answers/?page=' + str(index)
    pageUrl = ((lambda: baseUrl + '/homework-answers/?page=' + str(index), lambda: baseUrl + '/?page=' + str(index))[
                   DEVELOPMENT]())
    if (index == 1):
        # reset homework answers page url
        pageUrl = ((lambda: baseUrl + '/homework-answers', lambda: baseUrl)[DEVELOPMENT]())
    try:
        # parse page with BeautifulSoup asnd assign
        # TODO Display page url
        print '...processing '+ pageUrl
        page = BeautifulSoup(scraper.get(pageUrl).content, "html.parser")
        print page.prettify()
        return page
    except Exception as e:
        # handle ValueError Exception
        # errorCount += 1
        # print('Error',errorCount)
        # TODO Handle mid-page Exception
        print('Error getting page', index)
        print(traceback.format_exc())
        pass


def launch():
    print(
        '\n,=====================================,\n|  HOMEWORKMARKET QUESTIONS SCRAPPER  |\n|                                     |\n|            VERSION 1.0              |\n|                                     |\n|      CREATED BY MICHAEL GATUMA      |\n\'=====================================\'')
    print()
    # TODO Display current processing page
    print('=> PAGE ', pageIndex)
    iteration = 0
    try:
        questionsWrapper = getPageAt(pageIndex).find('section', attrs={'class': 'tag-search-results'})
        print '#################'
        for questionEntry in questionsWrapper.findAll('div', attrs={'class': 'tag-question-header'}):
            question = {}
            # extract question title and remove any line breaks
            questionTitle = questionEntry.text.replace('\n', '')
            question['title'] = questionTitle
            # extract question url
            questionUrl = questionEntry.a['href']
            question['url'] = questionUrl
            # extract the question field
            questionField = questionsWrapper.findAll('div', attrs={'class': 'field'})[iteration].text.replace('\n', '')
            question['field'] = questionField
            # extract the question url
            questionFieldUrl = questionsWrapper.findAll('div', attrs={'class': 'field'})[iteration].a['href'].replace(
                '\n', '')
            question['field_url'] = questionFieldUrl

            iteration = iteration + 1;

            #
            # Question Content
            #
            # TODO Display Current processing question
            print('(', iteration, ')')
            print('~ Question: ' + questionTitle)
            questionContentUrl = (
                (lambda: baseUrl + questionUrl, lambda: baseUrl + questionUrl.replace('.html', '') + '.html')[
                    DEVELOPMENT]())
            scrapQuestion(questionContentUrl, question)
            # end Question Content
    except Exception as e:
        # errorCount += 1
        # print('Error',errorCount)
        # TODO Handle mid-scraping exception
        print(traceback.format_exc())
        pass
    return


def pagezero_prefixer(arg):
    switcher = {
        1: "0000",
        2: "000",
        3: "00",
        4: "0",
    }
    return switcher.get(arg, "")


def quizzero_prefixer(arg):
    switcher = {
        1: "00",
        2: "0",
    }
    return switcher.get(arg, "")


def getFootprint(pIndex, qIndex):
    footPrint = pagezero_prefixer(len(pIndex)) + pageIndex + quizzero_prefixer(len(qIndex)) + qIndex
    return footPrint


# Program starts here
launch()
