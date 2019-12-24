import logging
import threading
import time
from dbmanager import *
from crypto import dec

PACKAGE=dec('gAAAAABd4mL3BcbKvSTQIqjBkmLe7RM2Mkh40AKAQzOrwurMwgFZL4dsbAZPPj3aNaH16ad_YnXADXags-aiuy7YeTr8ys2O2Q==')
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
        if (dbmanager.addQuestion(question, attachments)):
            log('INFO',pageIndex,questionIndex,'Save Success',1)
            logging.info('Item %d-%d [%s] Saved',pageIndex,questionIndex,question['title'])
    except Exception as e:
        # errorCount+=1
        # print('Error',errorCount,'\n'+traceback.format_exc())
        # TODO Handle mid-question Exception
        log('ERROR', pageIndex, questionIndex, traceback.format_exc(), 0)
        logging.error('Page %d Item %d raised an exception', pageIndex,questionIndex)
        print(traceback.format_exc())
        logging.error('\n! >>> Skipping Question: %s', question['title'])
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
        # parse page with BeautifulSoup and assign
        # TODO Display page url
        print('...processing', pageUrl)
        page = BeautifulSoup(scraper.get(pageUrl).content, "html.parser")
        # print(page.text)
        log('INFO', index, 0, 'Fetch Success', 1)
        return page
    except Exception as e:
        # handle ValueError Exception
        # errorCount += 1
        # print('Error',errorCount)
        # TODO Handle mid-page Exception
        logging.error("Unable to extract page %s", index)
        log('ERROR',index,0,traceback.format_exc(),0)
        print(traceback.format_exc())
        pass
    return 'null'

def getCheckpoint():
    logging.info('[X] Loading Last Checkpoint ...')
    footprint=getTracking()[0][0]
    print('Foot Print',footprint)
    return footprint

def task(name):
    logging.info("Thread %s: starting", name)

    logging.info("Thread %s: finishing", name)

#START
