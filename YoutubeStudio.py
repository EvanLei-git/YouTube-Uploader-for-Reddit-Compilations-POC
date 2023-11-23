from selenium  import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import undetected_chromedriver as ucChrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os,time
import configurations


from functions import myFilefunctions
myFilefunctions.ChromeReset()

try:
	chrome_temp_dir = os.path.abspath(configurations.CHROME_DATA_PATH)

	chrome_options = webdriver.ChromeOptions()
	#chrome_options.add_argument('--headless')
	#chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--disk-cache-size=0')
	#chrome_options.add_argument('--user-data-dir=C:\\your path\\User Data')
	chrome_options.add_argument('--user-data-dir='+chrome_temp_dir)
	chrome_options.add_argument('--profile-directory=Profile 6')
	#chrome_options.add_extension('ublock.crx')

	#chrome_options.add_argument(r'--user-data-dir=C:\\your path\\User Data')
	#chrome_options.add_argument(f'--profile-directory={"Profile 1"}') 
	# profile is one of 'Profile 1', 'Profile 2', etc
	#options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36")
	#driver = webdriver.Chrome(executable_path=r'C:\your path\chromedriver.exe')

	driver =ucChrome.Chrome(executable_path='./chromedriver.exe',options=chrome_options)
	driver.get("https://studio.youtube.com/channel/")
	time.sleep(1000000)
finally:
	pass
	#driver.quit()