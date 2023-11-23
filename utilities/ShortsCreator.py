from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.common.by import By
import undetected_chromedriver as ucChrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import pyperclip
import random
import os,sys
import logging
import time,datetime
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






	#main code







	try:
		myFilefunctions.fileReset(configurations.SHORT_PATH)
		#repeat checks for 3 shorts else dont upload
		counter=0
		audio=False
		mob_comp=False
		while counter<3 and (audio==False or mob_comp==False):
			if myDBfunctions.available_shorts_check()<50:
				print("cant find more than 50 shorts to upload",flush=True)
				break
			url,author,videolength,audioformat,videoformat,shortsUsage,title=myDBfunctions.randomShort()
			#print(url,author,videolength,audioformat,videoformat,shortsUsage,title)
			time.sleep(2)
			if myRedditWebfuntions.check_website_status(url) and myDBfunctions.available_shorts_check()>50:
				print("trying to download, ",url,flush=True)
				mob_comp =myVideoAudiofunctions.is_video_mobile_compatible(url+videoformat)
				#print (is_video_mobile_compatible(url+videoformat), url, videoformat)
				video_path = os.path.join(configurations.SHORT_PATH, 'short.mp4') 

				if mob_comp==True:
					os.system('ffmpeg -y -loglevel quiet -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i '+url+videoformat+' -i '+url+audioformat+' -af "pan=mono|c0=c0" '+video_path)
					time.sleep(2)
					audio =myVideoAudiofunctions.check_last_5_seconds_0db(video_path)


				checkcounter=0
				audio =myVideoAudiofunctions.check_last_5_seconds_0db(video_path)
				while (checkcounter<3 and audio==False):
					os.system('ffmpeg -y -loglevel quiet -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -headers "Referer: https://www.reddit.com" -user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" -i '+url+videoformat+' -i '+url+audioformat+' -af "pan=mono|c0=c0" '+video_path)
					time.sleep(2)
					audio =myVideoAudiofunctions.check_last_5_seconds_0db(video_path)
					time.sleep(2)
					checkcounter=checkcounter+1

				if audio==False:
					#print('There seems to be an issue with the sound of '+url)
					logging.info('There seems to be an issue with the sound of '+url)
					time.sleep(1)
				

			elif (myRedditWebfuntions.check_website_status("http://reddit.com")==True and myRedditWebfuntions.check_website_status(url)==False):
				myDBfunctions.remove_row(url,author)
			counter=counter+1
	except:
		logging.info("Error handling SHORT's URL or sound"+url)


	if audio==True and mob_comp==True:
		title += " #shorts"	


		try:
			with open(configurations.DEFAULT_VIDEO_INFO_PATH, 'rb') as f:
				json_data = f.read().decode('utf-8')

			# parse the JSON data
			data = json.loads(json_data)
			description = data['description']
			tags = ', '.join(['shorts'] + data['tags'])
			category = data['category']
		except:
			logging.info("Possibly Couldnt find DefaultVideoinfo.json")



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

		#chrome_options.add_argument(r'--user-data-dir=C:\\Users\\your path\\User Data')
		#chrome_options.add_argument(f'--profile-directory={"Profile 1"}') 
		# profile is one of 'Profile 1', 'Profile 2', etc
		#options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")
		#driver = webdriver.Chrome(executable_path=r'C:\Users\your path\chromedriver.exe')


		driver = ucChrome.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
		try:
		    driver.get("https://www.youtube.com/upload")
		    time.sleep(3)
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
		try:
			#create_button = driver.find_element('create-icon')
			#create_button.click() 
			create_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'create-icon')))
			create_button.click()
			time.sleep(1)
		except:
			logging.info('Problem with create-icon (First Click on page) ')

		time.sleep(1)
		
		try:
			#text_item = driver.find_element_by_id('text-item-0')
			#text_item.click()
			text_item = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'text-item-0')))
			text_item.click()
			time.sleep(1)
		except:
			logging.info('Problem with text-item-0 (Second Click on page) ')
		'''



		'''
		mySeleniumFunctions.__chooseVideo(video_path,driver)
		print(title,flush=True)
		mySeleniumFunctions.__titleUpdate(title,driver)
		mySeleniumFunctions.__descriptionUpdate(description,driver)
		mySeleniumFunctions.__notMadeForKids(driver)
		mySeleniumFunctions.__moreSettings(driver)
		if configurations.ADD_TAGS==True:
			mySeleniumFunctions.__tags(tags,driver)
		mySeleniumFunctions.__CategorySelect(category,driver)
		mySeleniumFunctions.__privatizeVideo(driver,0,True,url)

		time.sleep(4)

		driver.quit()
		
		time.sleep(2)


		'''


		__chooseVideo(video_path,driver)
		print(title,flush=True)
		__titleUpdate(title,driver)
		__descriptionUpdate(description,driver)
		__notMadeForKids(driver)
		__moreSettings(driver)
		if configurations.ADD_TAGS==True:
			__tags(tags,driver)
		__CategorySelect(category,driver)
		__privatizeVideo(driver,0,True,url)

		time.sleep(4)

		driver.quit()
		
		time.sleep(2)


		myFilefunctions.ChromeReset()

if __name__=="__main__":
	main()




#<input id="file-loader" hidden="true" type="file" class="style-scope ytcp-thumbnails-compact-editor-uploader-old" accept="image/jpeg,image/png">

# Wait for the desired text to appear on the website
#wait4SD = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'You can complete this step after the standard definition (SD) version of your video has been processed. While you wait, you can close this screen or go to the next step.')]"), "You can complete this step after the standard definition (SD) version of your video has been processed. While you wait, you can close this screen or go to the next step."))



#import end screen
#wait = WebDriverWait(driver, 10)
#button = wait.until(EC.element_to_be_clickable((By.ID, "import-from-video-button")))

# Click on the button
#button.click()





