import requests
import json
from itertools import repeat
import datetime
import time
import random
import subprocess
import os,sys
import praw
#from functools import partial
from multiprocessing import Pool,freeze_support
from inputimeout import inputimeout, TimeoutOccurred
from urllib.parse import urlparse
import logging
import importlib
#import VideoCreator
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


def randomize_list(lst):
    random.shuffle(lst)
    return lst

def multiprocessSubreddit(subreddit):
    try:

        print(subreddit,flush=True)
        for day in ['day','week','month','year']:
            print(subreddit,day,flush=True)
            link = 'https://www.reddit.com/r/'+subreddit+'/top/.json?t='+day+'&limit=100&domain="v.redd.it"'
            response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"},timeout=7)

            if response.status_code == 200:
                #data = json.loads(r.text, strict=False)
                data = response.json()
                data = data['data']['children']
                for submis in data:
                    over_18 = submis['data']['over_18']
                    title = submis['data']['title']
                    post_id = submis['data']['id']
                    url = submis['data']['url_overridden_by_dest']
                    author = submis['data']['author']
                    subreddit = submis['data']['subreddit']
                    created_utc = submis['data']['created_utc']
                    score=submis['data']['score']
                    #checking 
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
                                    #score=submission.score
                                    #print (score)
                                    if (myRedditWebfuntions.post_is_available(submission)==True) and (score>configurations.ALL_SCORE) and( not over_18):
                                        
                                        print(url,flush=True)
                                        sys.stdout.flush()

                                        month =myTimefunctions.extract_month(created_utc)
                                        year =myTimefunctions.extract_year(created_utc)
                                        newtitle=myRedditWebfuntions.remove_oc(title)
                                        alreadyExists=myDBfunctions.dataBaseHandler(url,post_id,author,length,audio,video,subreddit,month,year,newtitle,score)

                
                        elif (myRedditWebfuntions.check_website_status("http://reddit.com")==True and myRedditWebfuntions.check_website_status(url)==False):
                            time.sleep(3)
                            if myRedditWebfuntions.check_website_status(url):
                                pass
                            else:
                                pass
                                #myDBfunctions.remove_row(url,author)
    except Exception as e:
        print("Error message:", e)
        logging.info('issue with multiprocess: '+str(e))


#---------------------MAIN CODE------------------#


def main():
    
    #Making sure to create the log and database file if they dont exist
    myFilefunctions.initializing_logs(configurations.LOG_PATH)
    myFilefunctions.initializing_logs(configurations.DATABASE_PATH)

    #logging configuration setup
    logging.basicConfig(filename=configurations.LOG_PATH, level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('RedditScrapper has STARTED')

    #checking database size
    old_db_size = myDBfunctions.db_size_check()

    # log the file size
    logging.info('Database initial size: ' + str(old_db_size)) 
    count=0
    EndProccess=False
    while (EndProccess==False):

        subreddits=configurations.SUBREDDIT_LIST
        subreddits=randomize_list(subreddits)
        #middle = len(subreddits) // 2
        #sub1 = subreddits[:middle]
        #sub2 = subreddits[middle:]
        p = Pool(3)  
        until=myTimefunctions.randomDay()
        #shuffled_list = random.shuffle(subreddits)
        #p.starmap(multiprocessSubreddit, zip(subreddits, repeat(until)))

        p.starmap(multiprocessSubreddit, [(subreddit,) for subreddit in subreddits])
        #p.starmap(multiprocessSubreddit, [(sub, until) for sub in sub1])
        p.close()
        p.join()
        del p


        print(f'[{configurations.PAUSE_REDDIT_SCRAPPER} HOUR PAUSE]',flush=True)
        time.sleep(configurations.PAUSE_REDDIT_SCRAPPER* 3600)
         
        logging.info('RedditScrapper STARTING IN 10 MINUTES')
        print('[Starting in 10 mins]',flush=True) 
        time.sleep(600) 

        
        #myDBfunctions.removeDuplicates()

        '''
        DATABASE_PATH=configurations.DATABASE_PATH


        breakdata= myDBfunctions.db_size_check()
        logging.info('Database: '+str( myDBfunctions.db_size_check())+' added Data '+str( myDBfunctions.db_size_check() - old_db_size))
        

        print(f'[{configurations.PAUSE_REDDIT_SCRAPPER} HOUR PAUSE]',flush=True)
        time.sleep(configurations.PAUSE_REDDIT_SCRAPPER* 3600)
         
        logging.info('RedditScrapper STARTING IN 10 MINUTES')
        print('[Starting in 10 mins]',flush=True) 
        time.sleep(600) 

        importlib.reload(configurations)
        importlib.reload(credentials)
        os.system('cls')
        count=count+1
        print(f'cleared {count} times',flush=True)
        '''   
        
redditPRAW=praw.Reddit(
    client_id=credentials.prawid,
    client_secret=credentials.prawsecret,
    username=credentials.prawuser,
    #password=credentials.prawpass,
    user_agent=credentials.prawagent
    )
if __name__=="__main__":
    main()
    

    
