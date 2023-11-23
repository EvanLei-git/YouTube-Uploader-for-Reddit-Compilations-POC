from selenium  import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import undetected_chromedriver as ucChrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import os,sys
import logging
import time,datetime
import re
import json
sys.dont_write_bytecode = True

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import the configurations module
import configurations
from functions import myDBfunctions
from functions import myFilefunctions
from functions import myRedditWebfuntions
from functions import myTimefunctions
from functions import myVideoAudiofunctions
from functions import mySeleniumFunctions


def main():

    def __chooseVideo(video_path,driver):
        #upload Video
        try:
            video_file_path = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Filedata')))
            video_file_path.send_keys(video_path)
        except:
            
            print('Cant find id="Filedata" or cant find video file or file wasnt a video (mp4)')

        time.sleep(2)

    def __chooseThumbnail(thumbnail_path,driver):
        try:
            thumbnail_file_path = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'file-loader')))
            thumbnail_file_path.send_keys(thumbnail_path)
        except:
           print('Cant find id="file-loader" or cant find thunmbnail file or thumbnail didnt have the corrent extension png/jpg')

        time.sleep(1)

    def __titleUpdate(title,driver):
        try:
            time.sleep(5)
            pyperclip.copy(title)

            title_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#title-textarea #textbox')))
            # Clear the existing text content
            time.sleep(2)
            title_box.clear()
            # Enter new text content
            time.sleep(1)
            #title_box.send_keys(title) 
            title_box.click()
            #we have to copy paste it due to selenium not supporting emojis
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(2)


        except:
            print('Problem inserting title ')

    def __descriptionUpdate(description,driver):
        try:
            pyperclip.copy(description)
            description_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#description-textarea #textbox')))  
            time.sleep(2)  
            description_box.clear()
            time.sleep(1)
            description_box.click()
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(2)
        except:
            print('Problem inserting description ')

        time.sleep(1)

    def __notMadeForKids(driver):
        try:
            button_kids = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'VIDEO_MADE_FOR_KIDS_NOT_MFK')))
            button_kids.click()
            time.sleep(1) 
        except:
            print('Problem with clicking video NOT for kids button')

    time.sleep(1)

    def __moreSettings(driver):
        try:    
            morebutton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'toggle-button')))
            morebutton.click()
            time.sleep(1) 
        except:
            print('Couldnt click the open More settings')
        
    time.sleep(1)
    def __tags(taglist,driver):
        try: 
            tag_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Tags"]')))    
            tag_box.send_keys(taglist)
        except:
            print('Issue while inserting tags')

    time.sleep(1)

    def __CategorySelect(category,driver):
        try: 
            parent_elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'category')))
            child_elem = parent_elem.find_element(By.XPATH, ".//ytcp-dropdown-trigger")
            child_elem.click()
            time.sleep(1)
        except:
            print('Couldnt click the category list')

        try:
            try:
                comedy_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//yt-formatted-string[text()='{category}']")))
                comedy_element.click()
                time.sleep(10)
            except:
                print('Your category doesnt exist, tried to change it to Education')
                comedy_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//yt-formatted-string[text()='Education']")))
                comedy_element.click()
                time.sleep(10)
        except:
            print('Couldnt click any category, issue with list')
        
        time.sleep(3)


    #-------VIDEO ELEMENT PHASE (FOR END SCREEN)---------#

    def __chooseEndScreen(endscreenVideoName,driver):
        #changing the Tab to go to the VIDEO ELEMENTS
        try:
            VideoElementclick = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[test-id="VIDEO_ELEMENTS"]')))
            VideoElementclick.click()  
            time.sleep(1)
        except:
            print('Couldnt go to VIDEO ELEMENTS tab')

        time.sleep(2)

        try:
            wait = WebDriverWait(driver, 10)

            # Wait for the text to be present in the element
            element = wait.until(EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'You can complete this step after the standard definition (SD) version of your video has been processed. While you wait, you can close this screen or go to the next step.')]"), "You can complete this step after the standard definition (SD) version of your video has been processed. While you wait, you can close this screen or go to the next step."))

            while True:
                try:
                    # Wait for the text to disappear from the element
                    wait.until_not(EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'You can complete this step after the standard definition (SD) version of your video has been processed. While you wait, you can close this screen or go to the next step.')]"), "You can complete this step after the standard definition (SD) version of your video has been processed. While you wait, you can close this screen or go to the next step."))
                    #print("Text disappeared")
                    break
                except TimeoutException:
                    #print("Text still present")
                    time.sleep(5)
                    continue
        except:
            pass     
        #Pressing the import from video button for our end screen
        try:
            import_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'import-from-video-button')))
            import_button.click()
            time.sleep(1)
        except:
            print('Couldnt Click on the import from video button (to choose the end screen)...trying one more time')

        try:
            import_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'import-endscreen-from-video-button')))
            import_button2.click()
            time.sleep(1)
        except:
            print('Couldnt Click on the import from video button for the Second time ')

        #searching the title of the endscreen video
        try:
            time.sleep(2)
            search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search-yours')))
            search_input.clear()
            search_input.send_keys(configurations.END_SCREEN_SEARCH_WORD)
            #search_input.send_keys(Keys.RETURN)
            time.sleep(1)
        except:
            print('Couldnt Search '+configurations.END_SCREEN_SEARCH_WORD)


        #Pressing on the First video aka the video that has the name of the end screen we want to extract from
        try:
            time.sleep(2)
            # Find the video element with the tabindex="0" attribute
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ytcp-entity-card[tabindex="0"] #content')))
            element.click()
            time.sleep(1)
        except:
            print('Couldnt Find the Video or the Content element or couldnt press on it')
            time.sleep(1)
            try:
                time.sleep(2)
                closeImport = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'close')))
                closeImport.click()  
                time.sleep(1)
                closeImport = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'discard-button')))
                closeImport.click()  
            except:
                pass
        try:
            time.sleep(2)
            # Find the video element with the text "Random song"
            video_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'save-button')))
            # Click on the video element
            video_element.click()
            time.sleep(1)
        except:
            print('Couldnt Save the endscreen')
    #--------------CHECKS PHASE----------------#

    #Dont need anything here

    #---------VISIBILITY-REVIEW PHASE-----------#
    def __privatizeVideo(driver,uploadID,isShort,url):
        #changing the Tab to go to the VIDEO ELEMENTS
        try:
            time.sleep(2)
            VideoElementclick = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[test-id="REVIEW"]')))
            VideoElementclick.click()  
            time.sleep(1)
        except:
            print('Couldnt go to VIDEO ELEMENTS tab')

        #Marking Video as PRIVATE
        try:   
            visibility_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "PRIVATE")))
            visibility_button.click()    
        except:
            print('Couldnt click the private video button')




        #watting for upload, else if it passes the time in configurations.VIDEO_UPLOAD_WAIT_TIME then the upload will be cancelled
        start_time = datetime.datetime.now()
        if isShort==True:
            while True:
                try:
                    # Check if "Checks complete" message is visible

                    progress_label = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Checks complete')]")))
                    time.sleep(2)
                    done_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "done-button")))
                    done_button.click()
                    time.sleep(2)
                    myDBfunctions.shortsUsageSetup(url)
                    break
                except:
                    # Check if "Not ended" message is visible
                    try:
                        #Processing abandoned
                        abandonedError = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Processing abandoned')]")))                   
                        done_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "done-button")))
                        done_button.click()
                        print("Proccessing Error during the Upload",flush=True)
                        time.sleep(2)
                    except:
                        # Check if 6 hours have passed since the while loop started
                        elapsed_time = datetime.datetime.now() - start_time
                        if elapsed_time >= datetime.timedelta(hours=configurations.MAX_UPLOAD_SHORT_TIME):
                            print(f"{configurations.MAX_UPLOAD_SHORT_TIME} hours passed couldnt Upload",flush=True)
                            break
                        else:
                            time.sleep(30)
        else:
            while True:
                try:
                    # Check if "Checks complete" message is visible
                    progress_label = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Checks complete')]")))
                    time.sleep(2)
                    done_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "done-button")))
                    done_button.click()
                    time.sleep(2)
                    if configurations.AUTOMATIC_UPLOAD==False:
                        myFilefunctions.manualUploadIDsaver(configurations.MANUAL_UPLOAD_PATH,int(uploadID))
                    else:
                        myFilefunctions.updateVideoID(configurations.UPLOADID_PATH,int(uploadID))
                    break
                except:
                    # Check if "Not ended" message is visible
                    try:
                        abandonedError = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Processing abandoned')]")))   
                        done_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "done-button")))
                        done_button.click()
                        logging.info("Proccessing Error during the Upload")
                        time.sleep(2)
                    except:
                        # Check if 6 hours have passed since the while loop started
                        elapsed_time = datetime.datetime.now() - start_time
                        if elapsed_time >= datetime.timedelta(hours=configurations.MAX_UPLOAD_VIDEO_TIME):
                            print(f"{configurations.MAX_UPLOAD_VIDEO_TIME} hours passed couldnt Upload the #"+uploadID+" video")
                            break
                        else:
                            time.sleep(30)










    #---MAIN IS BELOW---

    #testing...
    #driver.get("https://google.com/")
    #time.sleep(200)

    #log_file = 'logs/Upload_Process.log'
    log_file = configurations.LOG_PATH
    myFilefunctions.initializing_logs(log_file)
   
    logging.basicConfig(filename=log_file, level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    # Log the start of the program
    logging.info('Upload Process has STARTED')

    uploadflag=True
    while uploadflag==True:
        if (configurations.AUTOMATIC_UPLOAD==True):

            vidNumber=int(myFilefunctions.getID(configurations.VIDEOID_PATH))
            uploadID=int(myFilefunctions.getID(configurations.UPLOADID_PATH))
            fileExists=True
            try:
                time.sleep(3)
                video_name = "CompilationV"+str(uploadID)+".mp4"
                video_path = os.path.abspath(os.path.join(configurations.READYVIDEOS_PATH, video_name))
                #print(video_path)
            except:
                fileExists=False
                uploadflag=False
                logging.info('File Doesnt Exist '+video_path )
                break

            if vidNumber<=uploadID or fileExists==False:
                logging.info('VideoID.txt > UploadID.txt, no videos available to upload')
                uploadflag=False
                break

        else:
            while True:
                uploadID = input("Enter a number or 'end' to quit: ")
                if uploadID == "end":
                    uploadflag=False
                    print("Exiting program...",flush=True)
                    break
                else:

                    try:
                        number = int(uploadID) #used as a check, if its not a number it will go to the except and repeat from start

                        if myFilefunctions.manualCheckNUM(configurations.MANUAL_UPLOAD_PATH, number)==True: #True means it might have been uploaded manually before
                            print(f"{configurations.MANUAL_UPLOAD_LIST} says video with number {uploadID} has been used before, do a check before continuing " ,flush=True)
                        else:
                            video_name = "CompilationV"+uploadID+".mp4"
                            video_path = os.path.abspath(os.path.join(configurations.READYVIDEOS_PATH, video_name))
                            if os.path.exists(video_path):
                                print(f"Video {video_name} was found, trying to upload it" ,flush=True)
                                uploadID=int(uploadID)
                                break
                            else:
                                print(f"Couldnt find video {video_name}, check if the file in this adress is correct \n -> {video_path}",flush=True)
                        
                    except ValueError:
                        print(f"You entered: {uploadID} maybe its not a number, try again",flush=True)



        if uploadflag==True:
            uploadID=str(uploadID)
            try:
                
                info_name = "ModifiedVideo"+uploadID+".json"
                info_path = os.path.abspath(os.path.join(configurations.READYVIDEOS_PATH, info_name))

                with open(info_path, 'rb') as f:
                    json_data = f.read().decode('utf-8')

            
                # parse the JSON data
                data = json.loads(json_data)

                # save each info
                title = data['title']
                description = data['description']
                tags = ', '.join(data['tags'])
                category = data['category']
            except:
                 logging.info("Possibly Couldnt find READY_VIDEOS/ModifiedVideo"+uploadID+".json")
                 title= "ha"
                 description= "yee"
                 tags="smart"
                 category='Education'


            chrome_temp_dir = os.path.abspath(configurations.CHROME_DATA_PATH)

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

            #chrome_options.add_argument(r'--user-data-dir=C:\\your path\\User Data')
            #chrome_options.add_argument(f'--profile-directory={"Profile 1"}') 
            # profile is one of 'Profile 1', 'Profile 2', etc
            #options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")
            #driver = webdriver.Chrome(executable_path=r'C:\your path\chromedriver.exe')


            try:
                driver = ucChrome.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
                driver.get("https://www.youtube.com/upload")
                time.sleep(5)
            except Exception as e:
                print("Error occurred while opening the first URL:", str(e))
            
            driver.quit()
            time.sleep(4)

            try:
                driver = ucChrome.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
                driver.get("https://www.youtube.com/upload")
                time.sleep(14)
            except Exception as e:
                print("Error occurred while opening the second URL:", str(e))


            #---------------------------------
            #------For Browsing purposes, deleting cookies,cache etc
            #change the sleep below to the seconds you need to log out and log back in and dont forget to change it back to normal
            time.sleep(1)
            #-------------------

            '''
            mySeleniumFunctions.__chooseVideo(video_path,driver)
            mySeleniumFunctions.__titleUpdate(title,driver)
            mySeleniumFunctions.__descriptionUpdate(description,driver)

            if os.path.exists(configurations.THUMBNAIL_PATH):
                PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
                thumb_path = os.path.join(configurations.THUMBNAIL_PATH, uploadID+'.jpg')
                if os.path.isfile(thumb_path):
                    mySeleniumFunctions.__chooseThumbnail(thumb_path,driver)

            mySeleniumFunctions.__notMadeForKids(driver)
            mySeleniumFunctions.__moreSettings(driver)
            if configurations.ADD_TAGS==True:
                mySeleniumFunctions.__tags(tags,driver)
            mySeleniumFunctions.__CategorySelect(category,driver)
            mySeleniumFunctions.__chooseEndScreen(configurations.END_SCREEN_SEARCH_WORD,driver)
            mySeleniumFunctions.__privatizeVideo(driver,uploadID,False,"nothing")

            uploadflag=False
            time.sleep(4)

            driver.quit()
            '''
            __chooseVideo(video_path,driver)
            __titleUpdate(title,driver)
            __descriptionUpdate(description,driver)

            if os.path.exists(configurations.THUMBNAIL_PATH):
                PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
                thumb_path = os.path.join(configurations.THUMBNAIL_PATH, uploadID+'.jpg')
                if os.path.isfile(thumb_path):
                    __chooseThumbnail(thumb_path,driver)

            __notMadeForKids(driver)
            __moreSettings(driver)
            if configurations.ADD_TAGS==True:
                __tags(tags,driver)
            __CategorySelect(category,driver)
            endscreen=configurations.END_SCREEN_SEARCH_WORD
            __chooseEndScreen(endscreen,driver)
            __privatizeVideo(driver,uploadID,False,"nothing")

            uploadflag=False
            time.sleep(4)

            driver.quit()

            time.sleep(2)
if __name__=="__main__":
    main()





