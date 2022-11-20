#! /home/gonzalo/RR/Programas/Rival-Regions/RR_Selm/tutorial-env/bin/python3

from MoE import resourceRenew, goldRenew, deepExploraiton, status, reset  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
from dotenv import load_dotenv
import os
import selenium
from helper import loginAccount, military_training, sendTG
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
import datetime
import requests



load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]
TOKEN = os.environ["telegram_token"]
chat_id = os.environ["telegram_chat_id"]

profile_path = '/home/gonzalo/.mozilla/firefox/06btiini.Turdetano'
service = Service('/usr/bin/geckodriver')

#add profile in options, try to use my firefox
options = Options()
#options = webdriver.FirefoxOptions()
#firefox_profile = FirefoxProfile('/home/gonzalo/.mozilla/firefox/hs1vtgtf.default-release-1654257641115')
options.add_argument("--disable-web-security")
#options.add_argument("-profile", "/home/gonzalo/.mozilla/firefox/hs1vtgtf.default-release-1654257641115")
options.add_argument("--disable-site-isolation-trials")
options.add_argument('--log-level=1')
options.add_argument("--lang=en")
options.add_argument("-profile")
options.add_argument(profile_path)
options.add_argument("--headless")
options.headless = True# Run without chrome ui 
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
#options.profile = firefox_profile




if __name__ == '__main__':
    #driver = uc.Chrome(options)
    driver = webdriver.Firefox(service=service, options=options)
        # chromeVersion = ChromeDriverManager().install()
        # driver = webdriver.Chrome(chromeVersion, chrome_options=options)
    driver.get("https://rivalregions.com") # The website we want to go to
    #path = os.path.abspath("/home/gonzalo/RR/Programas/Turdetano/violentmonkey-2.13.3.xpi")
    #driver.install_addon(path)
    time.sleep(3)
    
    #try:                        #Waits for cookie popup
    #    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//form/input[@name="mail"]')))
    #except Exception as e:
    #    print("Failed to initate",e)
    #    pass
    #loginAccount(driver)

    
    goldRenew(driver, TOKEN, chat_id)
    resourceRenew(driver, "oil")
    resourceRenew(driver, "ura")
    resourceRenew(driver, "dia")

    ct = str(datetime.datetime.now())

    message = "Full renew completed at "+ ct
    sendTG (TOKEN, chat_id, message)
    driver.close()
    driver.quit()

