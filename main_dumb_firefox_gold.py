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
from MoE import autodeep, goldRenew, reset, resourceRenew, status

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
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://rivalregions.com") # The website we want to go to
    time.sleep(3)
    
    #try:                        #Waits for cookie popup
    #    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//form/input[@name="mail"]')))
    #except Exception as e:
    #    print("Failed to initate",e)
    #    pass
    #loginAccount(driver)

    current_hour = datetime.datetime.now().hour


    goldRenew(driver,TOKEN,chat_id)

    startingtime = datetime.datetime.strptime("20-10-2019", '%d-%m-%Y')
    today = (datetime.datetime.today() - startingtime).days #it's not actually today, it's the days that have passed since the starting time
    repeatedRegions =[]

    with open('intoodeep.txt') as intoodeep:
        try:
            while True:
                line = intoodeep.readline()
                if not line:
                        break
                for line in intoodeep:
                    deepdata = line.split()
                    print("Deep: "+str(deepdata))
                    dayoftheweek = int(deepdata[0])
                    lastdeephour = int(deepdata[5])
                    lastdeepday= int(deepdata [4])
                    region = str(deepdata[1])
                    daysbetweenlastdeep = today - lastdeepday
                    
                    if datetime.date.today().isoweekday() == dayoftheweek  and region not in repeatedRegions:
                        print("Today is the day of the deep: "+str(dayoftheweek))
                        if daysbetweenlastdeep > 6 and int(current_hour) > lastdeephour:
                            print("and we can try to deep")
                            resourceList = ["gold", "oil", "ore", "uranium", "diamond"]
                            regionList = ["belfast", "cardiff", "channelislands","dublin","eastscotland", "edinburgh","faroeislands","gibraltar", "highlandsofscotland",
                            "iceland", "isleofman","london","midlandandwestireland","moonregion69","northsastscotland","northwestengland","northernireland","palau",
                            "southwestengland","southwestscotland","southandeastireland","swansea"]
                            repeatedRegions.append (deepdata[1])
                            resource = str(deepdata[2])
                            time.sleep(3)
                            locIndex = int(regionList.index(region.lower()))
                            resourceIndex = int(resourceList.index(resource.lower()))
                            autodeep(driver, locIndex, resourceIndex, deepdata,today,current_hour,TOKEN,chat_id)
                        else:
                            print ("but there is a deep until "+str(lastdeephour)+":00")
                    elif  region in repeatedRegions:
                        line = []  
                        break                         
                    else:
                        repeatedRegions.append (region)
                        print("Not today. Next recharge is in " + str(7 - daysbetweenlastdeep)+" days")
                        if lastdeephour == 23 and dayoftheweek != 7: #Sets deep for the next day if it's planned at 11:00 PM
                            deepdata[0]= str(int(deepdata[0])+1)
                            deepdata[5]=str(0)
                            pass
                            print("Deep date was moved from 11:00PM to 00:00 AM of the next day")
                        elif lastdeephour == 23 and dayoftheweek == 7: #Same as the last but for the special case of Sunday
                            deepdata[0]= str(1)
                            deepdata[5]=str(0)
                            pass
                            print("Deep date was moved from Sunday 11:00PM to Monday 00:00 AM")
                        else:
                            pass

                    if line is not None and line is not []:
                        line = ' '.join(deepdata)
                        print("Writing line: "+ str(line))
                        with open("temp.txt", "a") as tempfile:
                            tempfile.write(f'\n{line}')
        except Exception as e:
            message = f"Error while running AutoDeep for {Mail}. Traceback: {e}"
            sendTG (TOKEN, chat_id, message)

    os.replace('temp.txt', 'intoodeep.txt')

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
    driver.close()
    driver.quit()
    time.sleep(5)
    os.system(str(execute_script))

#-----------------------Syntax for the intoodeep.txt file----------

#PlannedDay Region(Complete Name) Resource(Name) Amount LastDayRecharged(int(lastdayrecharged - startingdate)) HourRecharged

#Regions: /Belfast - 0/Cardiff - 1/Channel Islands - 2/Dublin - 3/East Scotland - 4/Edinburgh - 5/
#Faroe Islands - 6/Gibraltar - 7/Highlands of Scotland - 8/Iceland - 9/Isle of Man - 10/
#London - 11/Midland and West Ireland - 12/Moon Region 69-13/North East Scotland - 14/
#North West England - 15/Northern Ireland - 16/Palau - 17/South West England - 18/
#South West Scotland - 19/South and East Ireland - 20/Swansea - 21/

#Resources: Gold Ore Uranium Diamond

#startingdate: 20-10-2019