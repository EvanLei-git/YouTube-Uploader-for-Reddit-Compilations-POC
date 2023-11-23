import os,sys



#------------Customizable------------#

SEARCH_DATE='2021-01-01'   #config= %Y-%m-%d its the minimum date you want the search to start

CLIP_MIN_TIME=6
CLIP_MAX_TIME=35

SHORT_SCORE=10000
ALL_SCORE=1000

#AUTOMATIC_UPLOAD=False
AUTOMATIC_UPLOAD=True

SUBREDDIT_LIST=["Catculations","CatsAreAssholes","FunnyAnimals","holdmycatnip","StartledCats","AnimalsBeingDerps"]

#time to Start the video with the newest clips of this month
NEWEST_START_VIDEO_TIME=200    #in seconds
#full length of video

#800 is better
FULL_VIDEO_TIME=800



END_SCREEN_SEARCH_WORD='End_Screen'

#ADD_TAGS=False
ADD_TAGS=True



	#################################################
	#-------DO NOT CHNAGE THE VALUES BELOW!!!-------#
	#################################################

#------Upload Wait limit------#	
PAUSE_REDDIT_SCRAPPER=2  #IN hours
VIDEO_UPLOAD_WAIT_TIME=0 #in hours
SHORT_UPLOAD_WAIT_TIME=0 #in hours


#------File/Folder settings------#	
#---------Max upload time before Cancel---#
MAX_UPLOAD_VIDEO_TIME=4
MAX_UPLOAD_SHORT_TIME=1
# Define the root directory of the package
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

CHROME_DATA_FOLDER ='Chrome_Temp_Data'
CHROME_DATA_PATH = os.path.join(PACKAGE_ROOT,CHROME_DATA_FOLDER)

CHROME_BACKUP_FOLDER ='Chrome_Backup_Data'
CHROME_BACKUP_PATH = os.path.join(PACKAGE_ROOT,CHROME_BACKUP_FOLDER)


MEDIAFOLDER_NAME ='MEDIA'

DATABASE_TABLE_NAME='RedditURLs'

DATABASE_FOLDER = 'database'
DATABASE_NAME = 'RedditURLs.db'
DATABASE_PATH = os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME, DATABASE_FOLDER, DATABASE_NAME)

ALLPOSTS_DATABASE='allposts.db'
ALLPOSTS_PATH = os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME, DATABASE_FOLDER, ALLPOSTS_DATABASE)

WATERMARK_FILE='watermark.png'
WATERMARK_PATH=os.path.join(PACKAGE_ROOT,WATERMARK_FILE)

LOG_FOLDER = 'logs'
LOG_NAME = 'RedditScrapper_run_status.log'
LOG_PATH = os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME, LOG_FOLDER, LOG_NAME)


READYVIDEOS_FOLDER='READY_VIDEOS'
READYVIDEOS_PATH = os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME,READYVIDEOS_FOLDER)


CURRENTVIDEOS_FOLDER='currentVideo'
CURRENTVIDEOS_PATH = os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME,CURRENTVIDEOS_FOLDER)

SHORT_FOLDER='currentShort'
SHORT_PATH = os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME,SHORT_FOLDER)

MANUAL_UPLOAD_LIST='ManualUploadList.txt'
MANUAL_UPLOAD_PATH=os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME,READYVIDEOS_FOLDER,MANUAL_UPLOAD_LIST)

VIDEOID_FILE='VideoID.txt'
VIDEOID_PATH= os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME,READYVIDEOS_FOLDER,VIDEOID_FILE)

UPLOADID_FILE='UploadID.txt'
UPLOADID_PATH= os.path.join(PACKAGE_ROOT,MEDIAFOLDER_NAME,READYVIDEOS_FOLDER,UPLOADID_FILE)

DEFAULT_VIDEO_INFO_FILE='DefaultVideoinfo.json'
DEFAULT_VIDEO_INFO_PATH=os.path.join(PACKAGE_ROOT,DEFAULT_VIDEO_INFO_FILE)


THUMBNAIL_FOLDER='thumbnails'
THUMBNAIL_PATH=os.path.join(PACKAGE_ROOT,THUMBNAIL_FOLDER)




sys.dont_write_bytecode = True







from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


chrome_temp_dir = os.path.abspath(CHROME_DATA_PATH)

chrome_options = webdriver.ChromeOptions()
#both of these for headless
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')

#chrome_options.add_argument('--disable-application-cache')
#chrome_options.add_argument('--disk-cache-size=0')
#chrome_options.add_argument('--user-data-dir=C:\\your path\\User Data')
chrome_options.add_argument('--user-data-dir='+chrome_temp_dir)
chrome_options.add_argument('--profile-directory=Profile 6')
#chrome_options.add_extension('ublock.crx')

#chrome_options.add_argument(r'--user-data-dir=C:\\Uyour path\\User Data')
#chrome_options.add_argument(f'--profile-directory={"Profile 1"}') 
# profile is one of 'Profile 1', 'Profile 2', etc
#options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")
#driver = webdriver.Chrome(executable_path=r'C:\Users\your path\chromedriver.exe')

