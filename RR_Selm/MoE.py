# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import schedule
from dotenv import load_dotenv
import os
from helper import loginAccount, goToParliament, select_law, state_exploration, accept_law

load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]

#------------------------------ Timed functions ------------------------------
def resourceRenew(driver, typeR="gol"):  #Code that executs after schedule 
    resources = ["gol", "oil", "ore", "ura", "dia"]
    ct = datetime.datetime.now()
    driver.get("https://rivalregions.com") # The website we want to go to
    time.sleep(3)
    print("Refilling ", typeR, ct)
    try:
        while True:
            goToParliament(driver)
            if accept_law(driver):
                break
            state_exploration(driver,resources.index(typeR))
            accept_law(driver) 
            break
    except:
        reset(driver, typeR)
def deepExploraiton(driver, locIndex, resource_index, amount):
    driver.get("https://rivalregions.com") # The website we want to go to
    try:
        while True:
            time.sleep(3)
            goToParliament(driver)
            # driver.get_screenshot_as_file("test.png")
            if(driver.current_url == "https://rivalregions.com/#parliament"):
                select_law(driver,3)
                driver.find_element(By.XPATH,'//div[@id="offer_dd_34_reg"]').click()
                regions=driver.find_elements(By.XPATH,'//div[@id="offer_dd_34_reg"]/ul/li')
                try:                        #Waits for element is clickable
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(regions[locIndex])).click() # try to click on the resource
                except:
                    print("Could not click, type resource error")
                    pass
                driver.find_element(By.XPATH,'//div[@id="offer_dd_34_res"]').click()
                resource_type=driver.find_elements(By.XPATH,'//div[@id="offer_dd_34_res"]/ul/li')
                try:                        #Waits for element is clickable
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(resource_type[resource_index])).click() # try to click on the resource
                except:
                    print("Could not click, type resource error")
                    pass
                l=driver.find_element(By.XPATH,'//div/input[@id="offer_count_34"]')
                l.clear()
                l.send_keys(str(amount))
                driver.find_element(By.XPATH, '//div[@id="offer_do"]').click()
                time.sleep(3)
                driver.implicitly_wait(1)
                # driver.get_screenshot_as_file("screenshot.png")
                try:                        #Waits for element is clickable
                    accept_law(driver)
                except Exception as e:
                    print("Could not click, type resource error", e)
                    pass
                break
    except: print("RIP")
def fuckzoco(driver, resource_index):
    driver.get("https://rivalregions.com") # The website we want to go to
    locIndex=0
    try:
        while locIndex<20: #creates a loop in order to refill every region except NI
            time.sleep(3)
            goToParliament(driver)
            # driver.get_screenshot_as_file("test.png")
            if(driver.current_url == "https://rivalregions.com/#parliament"):
                select_law(driver,1) #Selects plain resource exploration (second item)
                driver.find_element(By.XPATH,'//div[@id="offer_dd_18_reg"]').click()
                regions=driver.find_elements(By.XPATH,'//div[@id="offer_dd_18_reg"]/ul/li')
                try:                        #Waits for element is clickable
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(regions[locIndex])).click() # try to click on the resource
                except:
                    print("Could not click, type region error")
                    pass
                print("1")
                driver.find_element(By.XPATH,'//div[@id="offer_dd_18_res"]').click()
                resource_type=driver.find_elements(By.XPATH,'//div[@id="offer_dd_18_res"]/ul/li')
                print("2", resource_index)
                try:                        #Waits for element is clickable
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(resource_type[resource_index])).click() # try to click on the resource
                except:
                    print("Could not click, type resource error")
                    pass
                l=driver.find_element(By.XPATH,'//div/input[@id="offer_count_34"]')
                l=driver.find_element(By.XPATH,'//div/input[@id="offer_count_18"]')
                l.clear()
                driver.find_element(By.XPATH, '//div[@id="offer_do"]').click()
                time.sleep(3)
                driver.implicitly_wait(1)
                # driver.get_screenshot_as_file("screenshot.png")
                try:                        #Waits for element is clickable
                    accept_law(driver)
                    if locIndex == 14:
                        locIndex = 16
                    else:
                        locIndex=locIndex+1 #not sure if this will work
                except Exception as e:
                    print("Could not click, type resource error", e)
                    pass
                break
    except: print("RIP")

def status():
    ct = datetime.datetime.now()
    print("Alive", ct)
def reset(driver, typeR="default"): # type is where the code is comming from
    ct = datetime.datetime.now()    
    print("Doing a reset", ct)
    driver.delete_all_cookies()
    time.sleep(5)
    driver.get("https://rivalregions.com")
    time.sleep(5)
    try:
        loginAccount(driver)
        time.sleep(5)
    except:
        print("Failed to re-login")
        pass
    try:
        if typeR == "gol":
            resourceRenew(driver,"gol")
        elif typeR == "oil":
            resourceRenew(driver,"oil")
        elif typeR == "ura":
            resourceRenew(driver,"ura")
    except:
        print("Failed to bounce back")
        pass