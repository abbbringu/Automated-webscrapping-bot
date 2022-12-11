#! /home/gonzalo/RR/Programas/Rival-Regions/RR_Selm/tutorial-env/bin/python3
from __future__ import print_function

import datetime
import os
import time
from email import message
from multiprocessing.connection import wait

import psutil
import pygsheets
import requests
import selenium
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helper import (autoProfile, sendTG)
from MoE import autodeep, goldRenew, reset, resourceRenew, status, intoodeep, indexChecker


load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]
profile_path = os.environ["firefox_profile_path"]
service = Service(os.environ["geckodriver_path"])
execute_script = os.environ["execute_script"]

#---------------------------- Telegram Variables -----------------------------
TOKEN = os.environ["telegram_token"]
chat_id = os.environ["telegram_chat_id"]


#--------------------------- Geckodriver Options -----------------------------
options = Options()
options.add_argument("--disable-web-security")
options.add_argument("--disable-site-isolation-trials")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--log-level=1')
options.add_argument("--lang=en")
options.add_argument("-profile")
options.add_argument(profile_path)
options.add_argument("--headless")
options.headless = True# Run without chrome ui 
options.add_argument('--disable-gpu')  # Last I checked this was necessary.




if __name__ == '__main__':
    PROCNAME = "geckodriver" # or chromedriver or IEDriverServer
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
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


    fullReloadHours = [3,7,12,19,23]
    currentHour = datetime.datetime.now().hour
    goldRenew(driver, TOKEN, chat_id)

    if currentHour in fullReloadHours:
        resourceRenew(driver, "oil")
        resourceRenew(driver, "ura")
        resourceRenew(driver, "dia")
        ct = str(datetime.datetime.now())
        message = "Full renew completed at "+ ct
        sendTG (TOKEN, chat_id, message)
    
    
    elif currentHour == 18:
        indexChecker(driver,TOKEN, chat_id)


    
    
#---------------------------- Google Sheets Variables -----------------------------
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file']
    file_name = 'credentials.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
    client = pygsheets.authorize(service_account_file='credentials.json')
    spreadsheet = client.open_by_key(os.environ["spreadsheet_id"]) 
    worksheet = spreadsheet.worksheet_by_title("Turdetano") #You will need to change this
#----------------------------------------------------------------------------------
    autoProfile (driver, chat_id, TOKEN, Mail,worksheet)
    time.sleep(5)

    intoodeep(driver, currentHour, TOKEN, chat_id)

    #-----------------------Syntax for the intoodeep.txt file---------------------------------------

    #PlannedDay Region(Complete Name) Resource(Name) Amount LastDayRecharged(int(lastdayrecharged - startingdate)) HourRecharged

    #Regions: /Belfast - 0/Cardiff - 1/Channel Islands - 2/Dublin - 3/East Scotland - 4/Edinburgh - 5/
    #Faroe Islands - 6/Gibraltar - 7/Highlands of Scotland - 8/Iceland - 9/Isle of Man - 10/
    #London - 11/Midland and West Ireland - 12/Moon Region 69-13/North East Scotland - 14/
    #North West England - 15/Northern Ireland - 16/Palau - 17/South West England - 18/
    #South West Scotland - 19/South and East Ireland - 20/Swansea - 21/

    #Resources: Gold Ore Uranium Diamond

    #startingdate: 20-10-2019

    driver.close()
    driver.quit()
    
    if currentHour not in fullReloadHours:
        os.system(str(execute_script))
   


    


