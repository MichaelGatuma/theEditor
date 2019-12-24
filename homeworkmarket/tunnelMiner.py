import logging
import threading
import time
import traceback
import cfscrape
from bs4 import BeautifulSoup
import sys
from crypto import dec
import wpxmlrpc
from dbmanager import log,getLatestLog,recordwpmigration,wpmigrations

# create anti-cloudflare scraping object
scraper = cfscrape.create_scraper()
##constants
DEVELOPMENT = False;  # Debug Mode
baseUrl = ((lambda: 'https://www.homeworkmarket.com', lambda: 'https://www.hwmarket.com:4433')[DEVELOPMENT]())
attachments = []
pageIndex=1
questionIndex=0
PACKAGE=dec('gAAAAABd4mL3BcbKvSTQIqjBkmLe7RM2Mkh40AKAQzOrwurMwgFZL4dsbAZPPj3aNaH16ad_YnXADXags-aiuy7YeTr8ys2O2Q==')
def scrapQuestion(url, question):
    global questionIndex
    questionIndex += 1
    try:
        # TODO Display url of a question
        print '>>>', url
        # get and assign the page containing the question to a variable
        questionPage = scraper.get(url).content
        # parse with BeautifulSoup and get the question div tag
        content = BeautifulSoup(questionPage, 'html.parser').find('div', attrs={'class': 'question'})
        # get the question-body div tag and assign to a variable
        questionBody = content.find('div', attrs={'class': 'question-body'})
        # TODO Display the content of the question
        question['content'] = str(questionBody)
        #print('  ~ Content: ', ((lambda:"NULL", lambda:"OK")[len(questionBody)>0]))
        #print '  ~ Content: %s', str(questionBody)
        # get the attachment-list ul tag
        attachmentlist = content.find('ul', attrs={'class': 'attachment-list'})
        # get all the li tags and assign to a variable
        attachmentLinks = attachmentlist.findAll('li')

        # TODO Fetch attachments details
        #print '  ~ Attachments:',
        attachment = {}
        for attachmentLink in attachmentLinks:
            attachment['name'] = attachmentLink.text
            #print attachmentLink.text,
            attachment['url'] = baseUrl + attachmentLink.a['href'].replace('..', '')
            #print '<'+ baseUrl + attachmentLink.a['href'].replace('..', '', 1)+'>;',
            attachments.append(attachment)
        print
        print question['fields']
        #postid=wpxmlrpc.post(question['title'], question['fields'], str(questionBody), question['tags'])
        postid = wpxmlrpc.post(question['title'], ['Computer Science',], str(questionBody), 'Tags')
        if(postid==0):
            logging.error('Unable to post Item %d-%d [%s]',pageIndex,questionIndex,question['title'])
        else:
            logging.info('Item %d-%d [%s] Posted. Wordpress post_id : %s', pageIndex, questionIndex, question['title'],
                         postid)
            recordwpmigration(postid, getFootprint(pageIndex, questionIndex), url)

    except Exception as e:
        # errorCount+=1
        # print('Error',errorCount,'\n'+traceback.format_exc())
        # TODO Handle mid-question Exception
        log('ERROR', pageIndex, questionIndex, traceback.format_exc(), 0)
        logging.error('Page %d Item %d raised an exception', pageIndex,questionIndex)
        print traceback.format_exc()
        logging.error(' >>> Skipping Question: %s', question['title'])
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
        print '...processing '+pageUrl
        page = BeautifulSoup(scraper.get(pageUrl).content, "html.parser")
        # print(page.text)
        log('INFO', index, questionIndex, 'Fetch Success', 1)
        return page
    except Exception as e:
        # handle ValueError Exception
        # errorCount += 1
        # print('Error',errorCount)
        # TODO Handle mid-page Exception
        logging.error("Unable to extract page %s", index)
        log('ERROR',index,questionIndex,traceback.format_exc(),0)
        print traceback.format_exc()
        pass
    return 'null'

def getCheckpoint():
    footprint=getLatestLog()
    return footprint

def task(name):
    global pageIndex
    pageIndex=1
    time.sleep(1)
    logging.info("Main Thread starting")

    while wpmigrations()<PACKAGE:
        # TODO Display current processing page
        print('=> PAGE '+ str(pageIndex))
        iteration = 0
        try:
            questionsWrapper = getPageAt(pageIndex).find('section', attrs={'class': 'tag-search-results'})
            for questionEntry in questionsWrapper.findAll('div', attrs={'class': 'tag-question-header'}):
                question = {}
                # extract question title and remove any line breaks
                questionTitle = questionEntry.text.replace('\n', '')
                question['title'] = questionTitle
                # extract question url
                questionUrl = questionEntry.a['href']
                question['url'] = questionUrl
                # extract the question field
                questionFields = questionEntry.findAll('div', attrs={'class': 'field'})
                question['fields'] = questionFields
                #todo extract question tags
                question['tags']=['Tag 1', 'Tag 2']
                # extract the question url
                questionFieldUrl = questionsWrapper.findAll('div', attrs={'class': 'field'})[iteration].a[
                    'href'].replace(
                    '\n', '')
                question['field_url'] = questionFieldUrl

                iteration = iteration + 1;

                #
                # Question Content
                #
                # TODO Display Current processing question

                questionContentUrl = (
                    (lambda: baseUrl + questionUrl, lambda: baseUrl + questionUrl.replace('.html', '') + '.html')[
                        DEVELOPMENT]())
                if (iteration > questionIndex):
                    print '('+str(pageIndex)+'-'+str(iteration)+')'
                    print '~ Question: ' + questionTitle
                    scrapQuestion(questionContentUrl, question)
                # end Question Content
            pageIndex+=1
            # your script
            elapsed_time = time.time() - start_time
            time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            time.sleep(1000)
        except Exception as e:
            # errorCount += 1
            # print('Error',errorCount)
            # TODO Handle mid-scraping exception
            logging.error('Exception while exctracting data:')
            log('ERROR', pageIndex, questionIndex, traceback.format_exc(), 0)
            print traceback.format_exc()
            pass
    logging.info(dec('gAAAAABd4mL3BcbKvSTQIqjBkmLe7RM2Mkh40AKAQzOrwurMwgFZL4dsbAZPPj3aNaH16ad_YnXADXags-aiuy7YeTr8ys2O2Q=='),' Questions Satisfied!!')
    logging.info("Main Thread: finishing")

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
    footPrint = pagezero_prefixer(len(str(pIndex))) + str(pIndex) + quizzero_prefixer(len(str(qIndex))) + str(qIndex)
    return footPrint

def init():
    logging.info('[X] Loading Last Checkpoint ...')
    global pageIndex,questionIndex
    pageIndex=getCheckpoint()[3]
    questionIndex=getCheckpoint()[4]

#START
if __name__ == "__main__":
    global start_time
    start_time = time.time()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    print '\n,=====================================,\n|  HOMEWORKMARKET QUESTIONS SCRAPPER  |\n|                                     |\n|            VERSION 1.0              |\n|                                     |\n|      CREATED BY MICHAEL GATUMA      |\n\'=====================================\''
    print
    init()
    task('1')
    #mainThread = threading.Thread(target=task, args=('1'))
    #mainThread.start()
    #mainThread.join()
    #logging.info("Main    : all done")

