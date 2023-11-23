import sqlite3 as sl
import os,sys
import datetime
import time
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the configurations module
import configurations
sys.dont_write_bytecode = True


def randomShort():
    usedvideo=1
    counter=0
    usedvideoRetry=0
    
    #this will keep going 
    while usedvideoRetry>=0:
        con = sl.connect(configurations.DATABASE_PATH)
        c=con.cursor()
        c.execute(f"SELECT rowid,* FROM {configurations.DATABASE_TABLE_NAME} ORDER BY RANDOM() LIMIT 1;")
        c2=con.cursor()
        c2.execute(f"select max(rowid) from {configurations.DATABASE_TABLE_NAME}")
        #url,videolength,audioformat,videoformat,usedvideo
        mylist=list(c.fetchone())
        maxrows=c2.fetchone()[0]
        url=mylist[1]
        author=mylist[3]
        videolength=mylist[5]
        audioformat=mylist[6]
        videoformat=mylist[7]
        usedvideo=mylist[10]
        uploaID=mylist[11]
        shortsUsage=mylist[12]
        title=mylist[13]
        score=mylist[14]

        #i can add a usedvideo=0 so i dont reuse those in the main videos
        if shortsUsage==0 and len(title) > 9 and len(title) <90 and videolength>8 and score> configurations.SHORT_SCORE:
            return url,author,videolength,audioformat,videoformat,shortsUsage,title
    con.commit()
    con.close()
    return(0,0,0,0,0,0,0)

def available_shorts_check():
    try:
        # Open connection to SQLite database
        conn = sl.connect(configurations.DATABASE_PATH)

        # Execute SQL queries
        query1 = f"SELECT COUNT(*) FROM {configurations.DATABASE_TABLE_NAME} WHERE shortsUsage=0 AND usedvideo=0 AND LENGTH(title) > 9 AND LENGTH(title) < 90 AND videolength>8 AND score>{configurations.SHORT_SCORE} "
        count1 = conn.execute(query1).fetchone()[0]
        #query2 = f"SELECT COUNT(*) FROM {configurations.DATABASE_TABLE_NAME} WHERE uploadID=0"
        #count2 = conn.execute(query2).fetchone()[0]

        # Close connection to SQLite database
        conn.close()
        return count1
    except Exception as e:
        print("An error occurred:", e)
    conn.close()


def shortsUsageSetup(url):
    con = sl.connect(configurations.DATABASE_PATH)
    c3 = con.cursor()

    c3.execute(f"UPDATE {configurations.DATABASE_TABLE_NAME} set shortsUsage = ? where url = ?", (1, url))
    con.commit()
    con.close()


def removeDuplicates():
    db_filename=configurations.DATABASE_PATH
    try:
        con = sl.connect(db_filename)
        con.execute("""CREATE TABLE IF NOT EXISTS {table_name} (
                url TEXT,
                post_id TEXT,
                author TEXT,
                subreddit TEXT,
                videolength INTEGER,
                audioformat TEXT,
                videoformat TEXT,
                month INTEGER,
                year INTEGER,
                usedvideo INTEGER,
                uploadID INTEGER,
                shortsUsage INTEGER,
                title TEXT,
                score INTEGER
                );
            """.format(table_name=configurations.DATABASE_TABLE_NAME))
        con.commit()
    except:
        pass
    con = sl.connect(db_filename)
    c=con.cursor()
    c.execute("DELETE from {table_name} WHERE rowid not in( select  min(rowid) from {table_name} group by author,videolength)".format(table_name=configurations.DATABASE_TABLE_NAME))
    con.commit()
    con.close()

def dataBaseLength():
    db_filename=configurations.DATABASE_PATH
    con = sl.connect(db_filename)
    c2=con.cursor()
    c2.execute("select max(rowid) from {table_name}".format(table_name=configurations.DATABASE_TABLE_NAME))
    maxrows=c2.fetchone()[0]
    con.commit()
    con.close()
    return maxrows

'''
def usedvideoHandler(url, db_filename=configurations.DATABASE_PATH):
    con = sl.connect(db_filename)
    c3=con.cursor()    
    c3.execute("SELECT usedvideo FROM {table_name} WHERE url = ?".format(table_name=configurations.DATABASE_TABLE_NAME), (url,))
    usedvideo = c3.fetchone()[0]
    c3.execute("""UPDATE {table_name} set usedvideo = ? where url = ?""".format(table_name=configurations.DATABASE_TABLE_NAME),(usedvideo+1,url))
    con.commit()
    con.close()
    return 0
'''

def usedvideoHandler(url, db_filename=configurations.DATABASE_PATH, max_retries=5, retry_delay=1):
    con = None
    c3 = None
    retries = 0

    while retries < max_retries:
        try:
            con = sl.connect(db_filename)
            c3 = con.cursor()
            c3.execute("SELECT usedvideo FROM {table_name} WHERE url = ?".format(table_name=configurations.DATABASE_TABLE_NAME), (url,))
            result = c3.fetchone()

            if result is None:
                print("No rows found for URL: {0}. Retrying in {1} seconds...".format(url, retry_delay))
                time.sleep(retry_delay)
                retries += 1
            else:
                usedvideo = result[0]
                c3.execute("""UPDATE {table_name} SET usedvideo = ? WHERE url = ?""".format(table_name=configurations.DATABASE_TABLE_NAME), (usedvideo+1, url))
                con.commit()
                return 0

        except sl.DatabaseError as e:
            print("An error occurred:", str(e))
            break

        finally:
            if c3:
                c3.close()
            if con:
                con.close()

    print("Maximum number of retries reached. Unable to update database.")
    return -1

        
def available_clips_check():
    db_filename=configurations.DATABASE_PATH
    table_name=configurations.DATABASE_TABLE_NAME
    # Open connection to SQLite database
    conn = sl.connect(db_filename)

    # Execute SQL queries
    query1 = "SELECT COUNT(*) FROM {table_name} WHERE usedvideo=0 AND shortsUsage=0".format(table_name=table_name)
    count1 = conn.execute(query1).fetchone()[0]
    #query2 = "SELECT COUNT(*) FROM RedditURLs WHERE uploadID=0"
    #count2 = conn.execute(query2).fetchone()[0]

    # Close connection to SQLite database
    conn.close()
    return count1
    # Check counts and return result
    #if count1 > 100 and count2 > 100:
    #    return True
    #else:
    #    return False

def randomNewVideo():
    current_month = datetime.datetime.now().month
    last_month = (datetime.datetime.now() - timedelta(days=30)).month
    current_year = datetime.datetime.now().year
    
    con = sl.connect(configurations.DATABASE_PATH)
    c=con.cursor()
    
    # Count the number of videos that match the criteria
    c.execute(f"SELECT COUNT(*) FROM {configurations.DATABASE_TABLE_NAME} WHERE month IN ({current_month},{last_month}) AND year={current_year} AND usedvideo=0;")
    count = c.fetchone()[0]
    
    if count >= 30:
        # Select a random video that matches the criteria
        c.execute(f"SELECT rowid,* FROM {configurations.DATABASE_TABLE_NAME} WHERE month IN ({current_month},{last_month}) AND year={current_year} AND usedvideo=0 ORDER BY RANDOM() LIMIT 1;")
        mylist=list(c.fetchone())
        url=mylist[1]
        author=mylist[3]
        videolength=mylist[5]
        audioformat=mylist[6]
        videoformat=mylist[7]
        usedvideo=mylist[10]
        uploaID=mylist[11]
        con.commit()
        con.close()
        return url,author,videolength,audioformat,videoformat,usedvideo
    else:
        con.close()
        return randomVideo()

def randomVideo():
    usedvideo=1
    counter=0
    usedvideoRetry=0
    
    #this will keep going 
    while usedvideoRetry>=0:
        con = sl.connect(configurations.DATABASE_PATH)
        c=con.cursor()
        c.execute(f"SELECT rowid,* FROM {configurations.DATABASE_TABLE_NAME} WHERE usedvideo=0 ORDER BY RANDOM() LIMIT 1;")
        c2=con.cursor()
        c2.execute(f"SELECT max(rowid) FROM {configurations.DATABASE_TABLE_NAME}")
        #url,videolength,audioformat,videoformat,usedvideo
        mylist=list(c.fetchone())
        maxrows=c2.fetchone()[0]
        url=mylist[1]
        author=mylist[3]
        videolength=mylist[5]
        audioformat=mylist[6]
        videoformat=mylist[7]
        usedvideo=mylist[10]
        uploaID=mylist[11]
        con.commit()
        con.close()
        if usedvideo==usedvideoRetry:
            return url,author,videolength,audioformat,videoformat,usedvideo

        #this will make the code keep going 
        #elif counter>available_clips_check(configurations.DATABASE_PATH)*3:
        #    counter=0
        #    usedvideoRetry=usedvideoRetry+1
        else:
            counter=counter+1

    return(0,0,0,0,0,0)


def dataBaseHandler(url, post_id, author, videolength, audioformat, videoformat, subreddit, month, year, title, score):
   #dataBaseHandler(url, post_id, author, videolength, audioformat, videoformat, subreddit, month, year, title, score):
    table=configurations.DATABASE_TABLE_NAME
    try:
        con = sl.connect(configurations.DATABASE_PATH)
        try:
            con.execute(f"""CREATE TABLE {table} (
                    url TEXT,
                    post_id TEXT,
                    author TEXT,
                    subreddit TEXT,
                    videolength INTEGER,
                    audioformat TEXT,
                    videoformat TEXT,
                    month INTEGER,
                    year INTEGER,
                    usedvideo INTEGER,
                    uploadID INTEGER,
                    shortsUsage INTEGER,
                    title TEXT,
                    score INTEGER
                    );
                """)
            con.commit()
        except:
            nothing=0

        #creating cursor
        c=con.cursor()
     

        c.execute(f"SELECT rowid FROM {table} WHERE url = ?", (url,))
        data=c.fetchall()
        if len(data)==0:
            usedvideo=0
            uploadID=0
            shortsUsage=0
            params=(url, post_id, author, subreddit, videolength, audioformat, videoformat, month, year, usedvideo, uploadID, shortsUsage, title, score)
            c.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",params);
            con.commit()
            con.close()
            return(0)
        else:
            con.close()
            return(1)
    except Exception as e:
        print("An error occurred on line:", traceback.extract_tb(e.__traceback__)[0].lineno)
        print("Error message:", e)
        
def uploadIDsetup(url, newID):
    con = sl.connect(configurations.DATABASE_PATH)
    c = con.cursor()
    c.execute(f"SELECT uploadID FROM {configurations.DATABASE_TABLE_NAME} where url = ?", (url,))
    databaseUploadID = c.fetchone()[0]
    if databaseUploadID == 0:
        newuploadID = newID
    else:
        newuploadID = str(databaseUploadID) + "," + newID
    c3 = con.cursor()
    c3.execute(f"""UPDATE {configurations.DATABASE_TABLE_NAME} set uploadID = ? where url = ?""", (newuploadID, url))
    con.commit()
    con.close()

def remove_row(url, author):
    con = sl.connect(configurations.DATABASE_PATH)
    c = con.cursor()
    c.execute(f"DELETE FROM {configurations.DATABASE_TABLE_NAME} WHERE url=? AND author=?", (url, author))
    con.commit()
    con.close()

def check_record_exists(url,post_id,author):
    con = sl.connect(configurations.DATABASE_PATH)
    try:
        con.execute(f"""CREATE TABLE {configurations.DATABASE_TABLE_NAME} (
                url TEXT,
                post_id TEXT,
                author TEXT,
                subreddit TEXT,
                videolength INTEGER,
                audioformat TEXT,
                videoformat TEXT,
                month INTEGER,
                year INTEGER,
                usedvideo INTEGER,
                uploadID INTEGER,
                shortsUsage INTEGER,
                title TEXT,
                score INTEGER
                );
            """)
        con.commit()
    except:
        pass

    c3=con.cursor()    
    c3.execute(f"SELECT EXISTS(SELECT 1 FROM {configurations.DATABASE_TABLE_NAME} WHERE author=? AND post_id=? AND url=?)", (author, post_id, url,))
    result = c3.fetchone()

    c3.execute(f"SELECT COUNT(*) FROM {configurations.DATABASE_TABLE_NAME}")
    count = c3.fetchone()[0]

    con.commit()
    con.close()
    # return False if the table is empty, otherwise return True if the row exists
    return (count != 0 and result[0] == 1)

def db_size_check():
    databasePath=configurations.DATABASE_PATH
    #checking database size
    if os.path.isfile(databasePath):
        # get the size of the file in bytes
        db_size = os.path.getsize(databasePath) 
        return db_size
    else:
        return 0  #database doesnt exist, will be created in the future