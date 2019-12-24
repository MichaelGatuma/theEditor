import mysql.connector
import traceback
from crypto import dec
dbConnection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="library"
)

#creating database_cursor to perform SQL operation
dbCursor = dbConnection.cursor(buffered=True)
def addQuestion(question,attachments):
    global lastID
    query1='INSERT INTO posts(post_title, post_field, post_content, post_url, posted_at, due_on, budget) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    query2 = 'INSERT INTO attachments(post_id, name, url) VALUES (%s,%s,%s)'
    questionValues=(question['title'],question['field'],question['content'],question['url'],question['posted_at'],question['due_on'],question['budget'])

    try:
        #inserting the values
        dbCursor.execute(query1, questionValues)
        #commit the transaction
        dbConnection.commit()
        lastID=dbCursor.lastrowid
    except:
        print "Error. Rolling back now. <%s>",lastID
        dbConnection.rollback()
        print traceback.format_exc()
        return False
    try:
        print 'LastID: %s',lastID
        attachmentValues = (lastID, attachments['name'], attachments['url'])
        metaValues = (lastID)
        #inserting the values
        dbCursor.execute(query2, attachmentValues)
        #commit the transaction
        dbConnection.commit()
    except:
        print "Error. Rolling back now. <"+ dbCursor.lastrowid+ ">"
        dbConnection.rollback()
        print traceback.format_exc()
        return False
    print dbCursor.rowcount + " record(s) Inserted"
    dbConnection.close
    return True

def getTracking():
    query='SELECT footprint FROM app';
    footprint='00000000'
    try:
        dbCursor.execute(query)
        # commit the transaction
        footprint=dbCursor.fetchall()
    except:
        print traceback.format_exc()
        return footprint
    dbConnection.close
    return footprint

def setTracker(footprint,length):
    query='INSERT INTO app(footprint,length) VALUES(%s,%s)';
    values=(footprint,length)
    try:
        dbCursor.execute(query, values)
        # commit the transaction
        dbConnection.commit()
    except:
        print "Error. Rolling back now. <"+ dbCursor.lastrowid+ ">"
        dbConnection.rollback()
        print traceback.format_exc()
        return False
    dbConnection.close
    return true

def log(lvl,pgIndex,quizIndex,msg,state):
    query='INSERT INTO logs(level, page, question, stacktrace, success) VALUES(%s,%s,%s,%s,%s)'
    values=(lvl,pgIndex,quizIndex,msg,state)
    try:
        dbCursor.execute(query, values)
        dbConnection.commit()
    except:
        print "Fatal Error. Program will Terminate now..."
        print traceback.format_exc()
        #todo terminate program
    dbConnection.close

def getLatestLog():
    query='SELECT * FROM logs WHERE timestamp=(SELECT MAX(timestamp) FROM logs)';
    footprint=[]
    try:
        dbCursor.execute(query)
        # commit the transaction
        footprint=dbCursor.fetchone()
    except:
        print(traceback.format_exc())
        return footprint
    dbConnection.close
    return footprint

def recordwpmigration(postid,footprint,origin):
    query='INSERT INTO migration(post_id,footprint,origin) VALUES(%s,%s,%s)'
    values=(postid,footprint,origin)
    try:
        dbCursor.execute(query,values)
        dbConnection.commit()
    except:
        print "Unable to record migration"
        print traceback.format_exc()
        # todo terminate program
    dbConnection.close

def wpmigrations():
    query='SELECT * FROM migration'
    try:
        dbCursor.execute(query)
        return dbCursor.rowcount
    except:
        print traceback.format_exc()
        return dec('gAAAAABd4mL3BcbKvSTQIqjBkmLe7RM2Mkh40AKAQzOrwurMwgFZL4dsbAZPPj3aNaH16ad_YnXADXags-aiuy7YeTr8ys2O2Q==')