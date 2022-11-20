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
from helper import loginAccount, goToParliament, select_law, state_exploration, accept_law, gold_exploration, reboot, build_departments
import requests

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
            time.sleep(3)
            state_exploration(driver,resources.index(typeR))
            time.sleep(3)
            accept_law(driver) 
            break
    except:
        reset(driver, typeR)

def goldRenew(driver,TOKEN,chat_id):  #Code that executs after schedule 
    ct = str(datetime.datetime.now())
    time.sleep(3)
    message = "Attempting to renew at "+ ct
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(telegram_url).json())


    try:
        while True:
            goToParliament(driver)
            if accept_law(driver):
                break
            time.sleep(3)
            gold_exploration(driver)
            time.sleep(3)
            #custom accept law
            foundLaw = False
            accept_laws=["Resources explor", "Deep exploration"]
            laws = driver.find_elements(By.XPATH,'//div[@id="parliament_active_laws"]/div/div/div') # Get all active laws
            for n in laws:  # Find which is Resources exploration
                if len(n.get_attribute("innerText")) > 20:
                    if n.get_attribute("innerText")[0:16] in accept_laws:
                        print(str(n.get_attribute("innerText")[0:16]))
                        n.click()
                        foundLaw = True
                        break
                    elif n.get_attribute("innerText") [0:16] == "Hospital, Belfas":
                        message = "An error in law selection was spotted and corrected. Rebooting..."
                        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                        print(requests.get(telegram_url).json())
                        driver.find_element(By.XPATH,'//div[@class="button_red par_new_law cancel_law"]').click() # Click on cancel the law
                        reboot()

            time.sleep(2)
            if foundLaw:
                driver.find_element(By.XPATH,'//div[@id="offer_show_v"]/div/div[@url="pro"]').click() # Click on pro on the law
                message = "It should be finished"
                telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(telegram_url).json())
            return foundLaw
    except:
        goldReset(driver, chat_id, TOKEN)

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

def autodeep(driver, locIndex, resourceIndex,deepdata,today,current_hour,TOKEN,chat_id):
    driver.get("https://rivalregions.com") # The website we want to go to
    print(f"Attempting to deep explore {deepdata[2]} in {deepdata[1]}")
    message = (f"Attempting to deep explore {deepdata[3]} points of {deepdata[2]} in {deepdata[1]}")
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(telegram_url).json())
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
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(resource_type[resourceIndex])).click() # try to click on the resource
                except:
                    print("Could not click, type resource error")
                    pass
                l=driver.find_element(By.XPATH,'//div/input[@id="offer_count_34"]')
                l.clear()
                l.send_keys(str(deepdata[3]))
                driver.find_element(By.XPATH, '//div[@id="offer_do"]').click()
                time.sleep(3)
                driver.implicitly_wait(1)
                # driver.get_screenshot_as_file("screenshot.png")
                try:                        #Waits for element is clickable
                    #--------------------Custom Accept Deep Law-----------------------
                    foundLaw = False
                    laws = driver.find_elements(By.XPATH,'//div[@id="parliament_active_laws"]/div/div/div') # Get all active laws
                    for n in laws:  # Find which is Resources exploration
                        if len(n.get_attribute("innerText")) > 20:
                            if n.get_attribute("innerText")[0:16] in "Deep exploration":
                                n.click()
                                foundLaw = True
                                break
                    time.sleep(2)
                    if foundLaw:
                        driver.find_element(By.XPATH,'//div[@id="offer_show_v"]/div/div[@url="pro"]').click() # Click on pro on the law
                        deepdata[4]= str(today)
                        deepdata[5]= str(current_hour)
                        message = f"The deep exploration in {deepdata[1]} of {deepdata[2]} ({deepdata[3]}) was succesfully passed."
                        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                        print(requests.get(telegram_url).json())
                    return foundLaw
                except Exception as e:
                    message = f"There was a problem with the deep exploration in {deepdata[1]} of {deepdata[2]} ({deepdata[3]}). Please do it manually. Error: {e}"
                    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                    print(requests.get(telegram_url).json())
                    pass
                break
    except Exception as e: 
        print("RIP")
        message = f"There was a problem with the deep exploration in {deepdata[1]} of {deepdata[2]} ({deepdata[3]}). Please do it manually. Traceback: {e}"
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(telegram_url).json())
        pass

def fuckzoco(driver, resource_index):
    resource_index="gol"
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
                        print(locIndex, "region")
                    driver.refresh()
                    print("refrescado")
                except Exception as e:
                    print("Could not click, type resource error", e)
                    pass
                break
            print("i almost believed you")
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

def goldReset(driver, chat_id, TOKEN): # type is where the code is comming from
    ct = datetime.datetime.now()    
    print("Doing a reset", ct)
    message = f"Resetting at {ct}"
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(telegram_url).json())

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
        driver.quit()
        driver.close()
        reboot()
    except:
        print("Failed to bounce back")
        pass

