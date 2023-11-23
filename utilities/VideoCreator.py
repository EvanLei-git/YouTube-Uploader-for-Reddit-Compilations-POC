import json
from datetime import datetime
import time
import os,sys
import shutil
import importlib

#from functools import partial
import praw

#from inputimeout import inputimeout, TimeoutOccurred
import logging
import re

#same file utilities
import ShortsCreator
import SeleniumUploader
import Redditscrapper

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import the configurations module
import configurations
from functions import myDBfunctions
from functions import myFilefunctions
from functions import myRedditWebfuntions
from functions import myTimefunctions
from functions import myVideoAudiofunctions
sys.dont_write_bytecode = True


def main():
    while(True):
        #Making sure to create the log file if it doesnt exist
        myFilefunctions.initializing_logs(configurations.LOG_PATH)
        logging.basicConfig(filename=configurations.LOG_PATH, level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info('VideoCreator has STARTED')

        #print('Uploading Short', flush=True)
        #ShortsCreator.main()
        #print('Uploaded Short', flush=True)
        myFilefunctions.fileReset(configurations.CURRENTVIDEOS_PATH)
        newuploadID=myFilefunctions.getID(configurations.VIDEOID_PATH)
        vidtime=0
        newVideoList=[]
        clipcounter=0
        urlList=[] #used to remove url from the database only after the video is complete

        RedditDownFlag=False
        while vidtime <configurations.FULL_VIDEO_TIME:
           #get a random Video
            if vidtime<configurations.NEWEST_START_VIDEO_TIME:
                GetRandVideo = myDBfunctions.randomNewVideo
            else:
                GetRandVideo = myDBfunctions.randomVideo

            while True:
                url, author, videolength, audioformat, videoformat, usedvideo = GetRandVideo()

                # check if the random video still exists
                print("trying to download, ", url, flush=True)

                if myRedditWebfuntions.check_website_status(url):
                    if url in urlList:
                        continue  # try again if it's already in the list
                    urlList.append(url)  # save the url in the list
                    break  # break out of the loop if we found a valid url
                elif  myRedditWebfuntions.check_website_status("http://reddit.com")==False:
                    time.sleep(5)


            if myRedditWebfuntions.check_website_status(url):
                vidtime=vidtime+videolength
                newVideoList.append("clip"+str(clipcounter))
                video_path = os.path.join(configurations.CURRENTVIDEOS_PATH, 'clip'+str(clipcounter)+'.mp4') 
                #True  means its bigger than the res we are looking for
                bigger_res =myVideoAudiofunctions.is_video_bigger_than_16_9(url+videoformat)
                if bigger_res==True:
                    os.system('ffmpeg -y -loglevel quiet -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i '+url+videoformat+' -i '+url+audioformat+' -filter_complex "crop=in_h*16/9:in_h,scale=1920:-2" -af "pan=mono|c0=c0" '+video_path)
                
                else:
                    os.system('ffmpeg -y -loglevel quiet -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i '+url+videoformat+' -i '+url+audioformat+' -filter_complex "[0:v]scale=ih*16/9:-2,boxblur=luma_radius=min(h\,w)/10:luma_power=1:chroma_radius=min(cw\,ch)/10:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -af "pan=mono|c0=c0" -c:a aac -b:a 192k -async 1 '+video_path)
                    #random Test: ffmpeg -i DASH_720.mp4 -filter_complex "[0:v]scale=16/9,boxblur=15:15,setsar=1[bg];[bg][0]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -c:a copy out.mp4
                    #random Test: ffmpeg -i DASH_720.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" out4.mp4
                    #ffmpeg -reconnect_streamed 1 -i DASH_1080.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/10:luma_power=1:chroma_radius=min(cw\,ch)/10:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" out4.mp4

                    #at the 16/9:-1 i change the -1 to -2 so it will catch odd resolutions(i think)
                    #working current test: ffmpeg -y -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i https://v.redd.it/hwr330l9s8fa1/DASH_720.mp4 -i https://v.redd.it/hwr330l9s8fa1/DASH_audio.mp4 -filter_complex "[0:v]scale=ih*16/9:-2,boxblur=luma_radius=min(h\,w)/10:luma_power=1:chroma_radius=min(cw\,ch)/10:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" out4.mp4
                    


                    #Forth/current: ffmpeg -y -reconnect_streamed -reconnect_attempts 1  -i DASH_720.mp4 -filter_complex "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/10:luma_power=1:chroma_radius=min(cw\,ch)/10:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -af "pan=mono|c0=c0" out4.mp4
                    #Third: os.system('ffmpeg -y -i '+url+videoformat+' -i '+url+audioformat+' -vf "scale=1920:1080:force_original_aspect_ratio=decrease, pad=1920:1080:(ow-iw)/2 ,setsar=1,fps=fps=30,settb=AVTB,setpts=PTS-STARTPTS" -af "pan=mono|c0=c0" currentVideo/clip'+str(clipcounter)+'.mp4')
                    #Second,Old animals: os.system("ffmpeg -y -i "+url+videoformat+" -i "+url+audioformat+" -vf scale=1920:1080,setsar=16:9 -vcodec libx264 -pix_fmt yuv420p -crf 17 -s 1920x1080 -r 30 currentVideo/clip"+str(clipcounter)+".mp4")
                    #First: os.system("ffmpeg -i "+url+videoformat+" -i "+url+audioformat+" -vf scale=1920:1080  -crf 18 currentVideo/clip"+str(clipcounter)+".mp4")  


                    time.sleep(1)
                    ######zooming test######
                    
                    #"-vf", "crop=in_w:in_h-10,zoompan=z='zoom+0.20':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=hd1080"

                    os.system('ffmpeg -y -loglevel quiet -i '+video_path+' -vf "zoompan=z=\'zoom+0.40\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=hd1080,scale=1920:1080" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 192k '+video_path)
                    while not myVideoAudiofunctions.is_mp4_encoding_complete(video_path):
                        time.sleep(1)  # Sleep for 1 second before checking again

                time.sleep(3)
                audio =myVideoAudiofunctions.check_last_5_seconds_0db(video_path)
                checkcounter=0
                while (checkcounter<3 and audio==False):
                    if bigger_res==True:
                        os.system('ffmpeg -y -loglevel quiet -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i '+url+videoformat+' -i '+url+audioformat+' -filter_complex "crop=in_h*16/9:in_h,scale=1920:-2" -af "pan=mono|c0=c0" '+configurations.CURRENTVIDEOS_PATH+'/clip'+str(clipcounter)+'.mp4')
                        checkcounter=checkcounter+1
                        time.sleep(3)

                        while not myVideoAudiofunctions.is_mp4_encoding_complete(video_path):
                            time.sleep(1)  # Sleep for 1 second before checking again

                        audio =myVideoAudiofunctions.check_last_5_seconds_0db(video_path)
                    else:
                        os.system('ffmpeg -y -loglevel quiet -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i '+url+videoformat+' -i '+url+audioformat+' -filter_complex "[0:v]scale=ih*16/9:-2,boxblur=luma_radius=min(h\,w)/10:luma_power=1:chroma_radius=min(cw\,ch)/10:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16" -af "pan=mono|c0=c0" -c:a aac -b:a 192k -async 1 '+video_path)
                        checkcounter=checkcounter+1
                        time.sleep(2)
                        os.system('ffmpeg -y -loglevel quiet -i '+video_path+' -vf "zoompan=z=\'zoom+0.40\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=hd1080" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 192k '+video_path)
                        time.sleep(3)
                        while not myVideoAudiofunctions.is_mp4_encoding_complete(video_path):
                            time.sleep(1)  # Sleep for 1 second before checking again
                        audio =myVideoAudiofunctions.check_last_5_seconds_0db(video_path)
                        
                    time.sleep(1)
                if audio==False:
                    vidtime=vidtime-videolength
                    newVideoList.pop() #remove the last videoList
                    urlList.pop()    #remove last url
                    #maybe add -1 to the database usedvideo and shorts so i dont use the video in the future due to missing audio
                    logging.info('There seems to be an issue with the sound of '+url)
                    time.sleep(1)
                    if os.path.exists(configurations.CURRENTVIDEOS_PATH+'/clip'+str(clipcounter)+'.mp4'):
                        os.remove(configurations.CURRENTVIDEOS_PATH+'/clip'+str(clipcounter)+'.mp4')
                        time.sleep(3)
                else:
                    f  = open(configurations.CURRENTVIDEOS_PATH+'/mylist.txt', "a")
                    f.write("file 'clip"+str(clipcounter)+".mp4'\n")
                    f.close()

                    clipcounter=clipcounter+1

                
                
            #make sure reddit works before removing the link from the db
            elif  myRedditWebfuntions.check_website_status("http://reddit.com")==False:
                #making sure its not a computer/lag mistake
                time.sleep(5)
                if (myRedditWebfuntions.check_website_status("http://reddit.com")==False):
                    RedditDownFlag=True
                    logging.info('Reddit.com is down??? we have stopped this currentVideo, there is no need to change or stop anything, next video will be created later')
                    


            else:
                time.sleep(3)
                if myRedditWebfuntions.check_website_status(url):
                    pass
                else:
                    #remove row from db since video has been deleted from reddit
                    #myDBfunctions.remove_row(url,author)
                    pass
                    
        #if anim.available_clips_check(databasename):
            #do the above While 
        #else:
            #logging.info("Couldnt find 200 available clips, check DataBase for issues")
            #eror dont have 200 available clips
            #execute reddit scrapper

        if (RedditDownFlag==False):
            input_video = configurations.READYVIDEOS_PATH+'\\CompilationV'+newuploadID+'.mp4' 

            # Define a temporary output file path
            temp_output_video = configurations.READYVIDEOS_PATH+'\\CompilationV'+newuploadID+'_temp.mp4' 




            #connecting clips together
            newuploadID=str(newuploadID)
            os.system('ffmpeg -loglevel quiet -y -f concat -safe 0 -i '+configurations.CURRENTVIDEOS_PATH+'/mylist.txt -r 60 -vcodec libx264 -coder 1 -rc_lookahead 60 -threads 0 -shortest -avoid_negative_ts make_zero '+configurations.READYVIDEOS_PATH+'/CompilationV'+newuploadID+'.mp4')
            #print("test1")
            while not myVideoAudiofunctions.is_mp4_encoding_complete(input_video):
                time.sleep(1)  # Sleep for 1 second before checking again
            #WATERMARK EXAMPLE: os.system('ffmpeg -i CompilationV17.mp4 -i watermark.png -filter_complex "[1]format=rgba,colorchannelmixer=aa=0.03[logo];[0][logo]overlay=main_w-overlay_w-170:main_h-overlay_h-35:format=auto,format=yuv420p" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k output.mp4')
            #NOT SURE IF THE COMMAND UNDER THIS WORKS AS EXPECTED
            #os.system('ffmpeg -loglevel quiet -f concat -safe 0 -i '+configurations.CURRENTVIDEOS_PATH+'/mylist.txt -i '+configurations.WATERMARK_PATH+' -filter_complex [1]format=rgba,colorchannelmixer=aa=0.05[logo];[0][logo]overlay=main_w-overlay_w-170:main_h-overlay_h-35:format=auto,format=yuv420p -r 30 -vcodec libx264 -c:a aac -b:a 192k -coder 1 -threads 0 -avoid_negative_ts make_zero '+configurations.READYVIDEOS_PATH+'/CompilationV'+newuploadID+'.mp4')

            time.sleep(1)
            os.system('ffmpeg -loglevel quiet -y -i '+input_video+' -i '+configurations.WATERMARK_PATH+' -filter_complex "[1]format=rgba,colorchannelmixer=aa=0.04[logo];[0][logo]overlay=main_w-overlay_w-170:main_h-overlay_h-35:format=auto,format=yuv420p" -vcodec libx264 '+temp_output_video)
            #print("test2")
            while not myVideoAudiofunctions.is_mp4_encoding_complete(input_video):
                time.sleep(1)  # Sleep for 1 second before checking again
            time.sleep(2)
            if os.path.exists(input_video):
                os.remove(input_video)
            time.sleep(2)
            os.rename(temp_output_video,input_video)

            #optimising sound so it wont be as loud as the native(still not perfect)
            os.system("ffmpeg-normalize -f "+configurations.READYVIDEOS_PATH+"/CompilationV"+newuploadID+".mp4 -o "+configurations.READYVIDEOS_PATH+"/CompilationV"+newuploadID+".mp4 -c:a aac -b:a 192k ")
            #print("test3")
            while not myVideoAudiofunctions.is_mp4_encoding_complete(input_video):
                time.sleep(1)  # Sleep for 1 second before checking again
            #adding the information json to the READY_VIDEOS folder



            output_path = configurations.READYVIDEOS_PATH+'/ModifiedVideo'+newuploadID+'.json'
            # Copy the input file to the output directory
            shutil.copy(configurations.DEFAULT_VIDEO_INFO_PATH, output_path)
            time.sleep(3)
            #updating the json with the credits
            with open(output_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['credits'].extend(urlList)
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()

            # Open the output file and modify the title field
            with open(output_path, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data['title'] += newuploadID
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()

            #After ending with everything we have to update the Database...
            #changing the url's usedvideo value to +1 and adding the new upload ID to the videos
            for k in urlList:
                myDBfunctions.usedvideoHandler(k)
                myDBfunctions.uploadIDsetup(k,newuploadID)


            myFilefunctions.updateVideoID(configurations.VIDEOID_PATH,newuploadID)
            logging.info("Finished with Video "+newuploadID)
            #os.system('cls')
            

            time.sleep(5)
            if configurations.AUTOMATIC_UPLOAD==True:
                SeleniumUploader.main()
                time.sleep(2)
                myFilefunctions.ChromeReset()

            #time.sleep(600)  
            #logging.info('VideoCreator STARTING IN 10 MINUTES')
            #print('[Starting in 10 mins]',flush=True) 


            print('Pause for about ',configurations.SHORT_UPLOAD_WAIT_TIME,' hours before uploading the last Short',flush=True)
            time.sleep(configurations.SHORT_UPLOAD_WAIT_TIME*3600)
            print('[Starting in 10 mins]',flush=True) 
            time.sleep(600) 
            
            ShortsCreator.main()
            time.sleep(2)
            myFilefunctions.ChromeReset()

            print("\nUploaded last short, waiting ",configurations.VIDEO_UPLOAD_WAIT_TIME," hours.",flush=True)
            time.sleep(configurations.VIDEO_UPLOAD_WAIT_TIME*3600)
            print('[Starting in 10 mins]',flush=True) 
            time.sleep(600) 
            os.system('cls')
            importlib.reload(configurations)
        else:
            print('\n\n Reddit is Down.\n\n')


if __name__=="__main__":
    main()
