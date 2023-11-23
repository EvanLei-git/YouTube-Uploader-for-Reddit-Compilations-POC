import requests
import re
import os,sys
import subprocess
sys.dont_write_bytecode = True

def check_website_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def existanceCheck(link):
    #link example: "https://v.redd.it/i0tahd9vnpp22/"
    vidextensions=["/DASH_1080.mp4","/DASH_720.mp4","/DASH_480.mp4","/DASH_9_6_M","/DASH_2_4_M"]
    audioextensions=["/DASH_audio.mp4","/audio"]
    videxists=False
    vidcounter=0
    while (videxists==False and vidcounter<(len(vidextensions))):
        h = requests.head(link+vidextensions[vidcounter])
        header = h.headers
        file_type = header.get('content-type')
        #respond = requests.get(link+vidextensions[vidcounter])
        #file_type = respond.headers['content-type']
        file_type=str(file_type)[-3:]
        if file_type ==("mp4"):
            videxists=True
            #print ("MP4 BABY")
            #print(file_type)
            break
        else:
            #print (vidextensions[vidcounter],"XML ewww")
            vidcounter=vidcounter+1

            
    audiocounter=0
    audioexists=False
    while (videxists==True and (audioexists==False and audiocounter<len(audioextensions))):
        respond = requests.get(link+audioextensions[audiocounter])
        file_type = respond.headers['content-type']
        file_type=file_type[-3:]
        if file_type ==("mp4"):
            #print ("MP3 BABY")
            audioexists=True
            break
        else:
            #print (audioexists,"XML ewww")
            audiocounter=audiocounter+1

        
    if (audioexists==True and videxists==True):
        return vidextensions[vidcounter],audioextensions[audiocounter]
    else:
        return "no","no"

    


#checking if post is removed
def post_is_available(post):
    return post.removed_by_category is None

def remove_oc(title):
    # remove [OC], (OC), or standalone OC in any case
    title = re.sub(r'\[OC\]|\(OC\)|\bOC\b', '', title, flags=re.IGNORECASE).strip()
    title = re.sub(r'\s*\bmy\b\s*', ' ', title, flags=re.IGNORECASE).strip()

    return title
