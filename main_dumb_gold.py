#! /home/gonzalo/RR/Programas/Rival-Regions/RR_Selm/tutorial-env/bin/python3

import os
from dotenv import load_dotenv
from MoE import resourceRenew, deepExploraiton, status, reset
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
from helper import loginAccount

load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]

options = Options()
options.add_argument("--disable-web-security")
options.add_argument("--disable-site-isolation-trials")
options.add_argument('--log-level=1')
options.add_argument("--lang=en")
options.headless = True# Run without chrome ui 
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

if __name__ == '__main__':
    driver = uc.Chrome(options)
        # chromeVersion = ChromeDriverManager().install()
        # driver = webdriver.Chrome(chromeVersion, chrome_options=options)
    driver.get("https://rivalregions.com") # The website we want to go to
    time.sleep(3)
    try:                        #Waits for cookie popup
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//form/input[@name="mail"]')))
    except Exception as e:
        print("Failed to initate",e)
        pass
    loginAccount(driver)
    resourceRenew(driver)
    driver.close()
    driver.quit()
