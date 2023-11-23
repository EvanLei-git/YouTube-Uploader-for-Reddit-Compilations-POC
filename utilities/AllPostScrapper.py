import requests
import json
from itertools import repeat
import datetime
import time
import random
import subprocess
import os,sys
import praw
import sqlite3
#from functools import partial
from multiprocessing import Pool,freeze_support
from inputimeout import inputimeout, TimeoutOccurred
from urllib.parse import urlparse
import logging
import importlib
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the configurations module
import configurations
from credentials import credentials
from functions import myDBfunctions
from functions import myFilefunctions
from functions import myRedditWebfuntions
from functions import myTimefunctions
from functions import myVideoAudiofunctions

sys.dont_write_bytecode = True

def process_submission(submission):
    try:
        url, post_id, author, subreddit, created_utc, title = submission
        title = "." if title is None else title  
        time.sleep(1)

        conn = sqlite3.connect(configurations.ALLPOSTS_PATH)
        cursor = conn.cursor()
        checkedflag=False
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'v.redd.it':
            #cmd check
            #print("before check "+url)
            if (myDBfunctions.check_record_exists(url,post_id,author)==False):
                time.sleep(1)
                #print("doesnt exist "+url)
                video,audio= myRedditWebfuntions.existanceCheck(url)
                if audio!="no":
                    #print("audio check complete "+url)
                    length=myVideoAudiofunctions.getVideoLength(str(url),str(audio))
                    time.sleep(1)
                    if (configurations.CLIP_MIN_TIME<= int(length) and int(length)  <=configurations.CLIP_MAX_TIME):
                        #print("length check "+url)
                        #checking if video is removed by moderator
                        submission=redditPRAW.submission(id=post_id)
                        score=submission.score
                        #print (score)
                        if (myRedditWebfuntions.post_is_available(submission)==True) and (score>configurations.ALL_SCORE) and( not submission.over_18):
                            
                            checkedflag=True
                            print(url,flush=True)
                            sys.stdout.flush()

                            month =myTimefunctions.extract_month(created_utc)
                            year =myTimefunctions.extract_year(created_utc)
                            newtitle=myRedditWebfuntions.remove_oc(title)
                            cursor.execute("UPDATE data SET checked = 2 WHERE url = ?", (url,))
                            conn.commit()
                            conn.close()  
                            alreadyExists=myDBfunctions.dataBaseHandler(url,post_id,author,length,audio,video,subreddit,month,year,newtitle,score)

                            

            elif (myRedditWebfuntions.check_website_status("http://reddit.com")==True and myRedditWebfuntions.check_website_status(url)==False):
                cursor.execute("DELETE FROM data WHERE url = ?", (url,))
                conn.commit()
                
                checkedflag = True

        if checkedflag==False:
            cursor.execute("UPDATE data SET checked = 1 WHERE url = ?", (url,))
            conn.commit()
        conn.close()          
    except Exception as e:
        print("Error message:", e)
        logging.info('issue with multiprocess: '+str(e))

if __name__ == '__main__':
    redditPRAW=praw.Reddit(
        client_id=credentials.prawid,
        client_secret=credentials.prawsecret,
        username=credentials.prawuser,
        #password=credentials.prawpass,
        user_agent=credentials.prawagent
        )
    while(True):
        # Connect to the merged database
        conn = sqlite3.connect(configurations.ALLPOSTS_PATH)
        cursor = conn.cursor()
        statusTest="6v03tj"
        submission=redditPRAW.submission(id=statusTest)
        print(submission.score)
        # Fetch 2000 URLs where the 'checked' column is 0
        cursor.execute("SELECT url, post_id, author, subreddit, created_utc, title FROM data WHERE checked = 0 LIMIT 1000")
        rows = cursor.fetchall()

        # Close the connection and cursor
        conn.close()
        # Process submissions using a process pool with 4 workers
        with Pool(4) as pool:
            pool.map(process_submission, rows)

        conn.close() 

        #logging.info('STARTING IN 10 MINUTES')
        #print('[Starting in 10 mins]',flush=True) 
        #time.sleep(600)


redditPRAW=praw.Reddit(
    client_id=credentials.prawid,
    client_secret=credentials.prawsecret,
    username=credentials.prawuser,
    #password=credentials.prawpass,
    user_agent=credentials.prawagent
    )