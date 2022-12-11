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
from helper import loginAccount, goToParliament, select_law, state_exploration, accept_law, gold_exploration, reboot, build_departments, sendTG, check_exists_by_xpath
import requests
from math import log, floor

load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]

#------------------------------ Timed functions ------------------------------
def resourceRenew(driver  , typeR="gol"):  #Code that executs after schedule 
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
            state_exploration(driver  ,resources.index(typeR))
            time.sleep(3)
            accept_law(driver) 
            break
    except:
        reset(driver, typeR)

def goldRenew(driver  ,TOKEN,chat_id):  #Code that executs after schedule 
    ct = str(datetime.datetime.now())
    time.sleep(3)
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
                        sendTG (TOKEN, chat_id, message)
                        driver.find_element(By.XPATH,'//div[@class="button_red par_new_law cancel_law"]').click() # Click on cancel the law
                        reboot()

            time.sleep(2)
            if foundLaw:
                driver.find_element(By.XPATH,'//div[@id="offer_show_v"]/div/div[@url="pro"]').click() # Click on pro on the law
                message = "Gold was renewed at "+ct
                sendTG (TOKEN, chat_id, message)
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

def intoodeep(driver, currentHour, TOKEN, chat_id):
    with open('intoodeep.txt') as intoodeep:
        startingtime = datetime.datetime.strptime("20-10-2019", '%d-%m-%Y')
        today = (datetime.datetime.today() - startingtime).days #it's not actually today, it's the days that have passed since the starting time
        repeatedRegions =[]
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
                        if daysbetweenlastdeep > 6 and int(currentHour) > lastdeephour:
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
                            autodeep(driver, locIndex, resourceIndex, deepdata,today,currentHour,TOKEN,chat_id)
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

def autodeep(driver, locIndex, resourceIndex,deepdata,today,currentHour,TOKEN,chat_id):
    driver.get("https://rivalregions.com") # The website we want to go to
    print(f"Attempting to deep explore {deepdata[2]} in {deepdata[1]}")
    message = (f"Attempting to deep explore {deepdata[3]} points of {deepdata[2]} in {deepdata[1]}")
    sendTG (TOKEN, chat_id, message)
    try:
        while True:
            time.sleep(3)
            goToParliament(driver)
            # driver.get_screenshot_as_file("test.png")
            if(driver.current_url == "https://rivalregions.com/#parliament"):
                select_law(driver,3)
                time.sleep(3)
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH,'//div[@id="offer_dd_34_reg"]').click()
                driver.implicitly_wait(10)
                regions=driver.find_elements(By.XPATH,'//div[@id="offer_dd_34_reg"]/ul/li')
                try:                        #Waits for element is clickable
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(regions[locIndex])).click() # try to click on the resource
                except:
                    print("Could not click, type resource error")
                    pass
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH,'//div[@id="offer_dd_34_res"]').click()
                driver.implicitly_wait(10)
                resource_type=driver.find_elements(By.XPATH,'//div[@id="offer_dd_34_res"]/ul/li')
                try:                        #Waits for element is clickable
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(resource_type[resourceIndex])).click() # try to click on the resource
                except:
                    print("Could not click, type resource error")
                    pass
                driver.implicitly_wait(10)
                l=driver.find_element(By.XPATH,'//div/input[@id="offer_count_34"]')
                l.clear()
                l.send_keys(str(deepdata[3]))
                driver.implicitly_wait(10)
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
                        deepdata[5]= str(currentHour)
                        message = f"The deep exploration in {deepdata[1]} of {deepdata[2]} ({deepdata[3]}) was successfully passed."
                        sendTG (TOKEN, chat_id, message)
                    return foundLaw
                except Exception as e:
                    message = f"There was a problem with the deep exploration in {deepdata[1]} of {deepdata[2]} ({deepdata[3]}). Please do it manually. Error: {e}"
                    sendTG (TOKEN, chat_id, message)
                    pass
                break
    except Exception as e: 
        print("RIP")
        message = f"There was a problem with the deep exploration in {deepdata[1]} of {deepdata[2]} ({deepdata[3]}). Please do it manually. Traceback: {e}"
        sendTG (TOKEN, chat_id, message)
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

def autopay(driver,worksheet):
    returnMoneyList = worksheet.get_col(14, include_tailing_empty=False)
    index=0
    for returnMoney in returnMoneyList:
        index = index+1
        print(index)
        taxPayerLink = worksheet.get_value(f"B{index}")
        notNumber=False
        try:
            returnMoney= str(float(returnMoney)*10**9)
        except:
            print(returnMoney)
            returnMoney= "0"
        print(returnMoney)
        if returnMoney == "0" or returnMoney == "" or returnMoney == None:
            print(f"{taxPayerLink} doesn't have money to return: {returnMoney}")
        else:
            print(f"{taxPayerLink} needs to be returned {returnMoney} €")
            payDecision = input("Pay? [Y/N]: ")
            if payDecision == "Y":
                print(f"{payDecision} : Attempting to pay {returnMoney} to {taxPayerLink}")
                sendMoney (driver,taxPayerLink, returnMoney)
            else:
                print("Canceled: " + payDecision)
            

def sendMoney (driver,link, quantity):
    try:
        driver.get(link)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='slide_profile_add_donate']"))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='small storage_number_change'][@url='0']"))).click()
        l=driver.find_element(By.XPATH,'//div/input[@class="imp donate_amount storage_sell_ammount tc white tpbg"]')
        l.clear()
        l.send_keys(str(quantity))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='donate_sell_button button_green']"))).click()


    except Exception as e:
        print( f"Error while sending money for {link}. Traceback: {e}")


def indexChecker(driver,TOKEN, chat_id):
    stateID="3046"
    driver.get(f"https://rivalregions.com/info/regions/{stateID}")
    underdevelopedRegions=[]
    regionNumber ="1"
    while check_exists_by_xpath(driver,f"/html/body/table/tbody/tr[{regionNumber}]")==True:
        devIndex = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/table/tbody/tr[{regionNumber}]/td[34]'))).get_attribute("textContent")
        if int(devIndex) < 6:
            regionName = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,f'/html/body/table/tbody/tr[{regionNumber}]/td[1]/a'))).get_attribute("textContent")[:-10]
            print(regionName +": " +devIndex)
            regionName = "".join(regionName.split())
            underdevelopedRegions.append(regionName)
        regionNumber=str(int(regionNumber)+1)
    print(underdevelopedRegions)
    message=f"Undeveloped regions in the State {underdevelopedRegions}"
    sendTG (TOKEN, chat_id, message)
    if underdevelopedRegions != []:
        autoHouseBuilder(driver, underdevelopedRegions, TOKEN,chat_id)


def autoHouseBuilder(driver, underdevelopedRegions, TOKEN,chat_id):
    driver.get("https://rivalregions.com/#listed/country/-2/0/homes") # The website we want to go to
    time.sleep(20)
    regionList = ["belfast", "cardiff", "channelislands","dublin","eastscotland", "edinburgh","faroeislands","gibraltar", "highlandsofscotland",
    "iceland", "isleofman","london","midlandandwestireland","moonregion69","northsastscotland","northwestengland","northernireland","palau",
    "southwestengland","southwestscotland","southandeastireland","swansea"]
    skippedRegions= ["belfast"]
    houseObjective = str(int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,f'//td[@class="list_level tip yellow"][contains(text(),"6")]/following-sibling::td'))).get_attribute("textContent"))+20)
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='slide_close']"))).click() #close autotab
    except:
        close = driver.find_element(By.XPATH,"//div[@id='slide_close']") 
        driver.execute_script("arguments[0].click();", close)
    print(f"Attempting to reach {houseObjective} houses in {underdevelopedRegions}")
    try:
        for region in underdevelopedRegions:
            if (region.lower()) not in skippedRegions:
                locIndex = str(int(regionList.index(region.lower()))+1)
                print(locIndex)
                time.sleep(3)
                if(driver.current_url != "https://rivalregions.com/#parliament"):
                    goToParliament(driver)
                    driver.implicitly_wait(20)
                if check_exists_by_xpath(driver,'//div[@class="button_red par_new_law cancel_law"]')==True:
                    driver.find_element(By.XPATH,'//div[@class="button_red par_new_law cancel_law"]').click()
                    time.sleep(3)
                driver.find_element(By.XPATH,'//div[@action="parliament/offer"]').click()
                time.sleep(5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="offer_dd_building"][@class="dd-container"]'))).click()
                driver.implicitly_wait(5)
                #element = driver.find_element("xpath", f"//div[@url='{url}'][@class='float_left hov2 pointer inst_plus green']") #find element and scroll down in case it is needed
                #element.location_once_scrolled_into_view
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="dd-option-text"][contains(text(),"House fund")]'))).click() #clicks houses
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="offer_dd_state_select_build"][@class="dd-container"]'))).click()
                #try:                        #Waits for element is clickable
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[3]/div/div[3]/div[8]/div[4]/div[2]/div/ul/li[{locIndex}]"))).click() # try to click on region(doesnot work)
                #except:
                    #print("Could not click, region error")
                    #pass
                housesNow=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,f'//span[@id="build_3_sum"]'))).get_attribute("textContent")
                housesNeeded = str(int(houseObjective)- int(housesNow)+1)
                l=driver.find_element(By.XPATH,'//div/input[@id="offer_count_build"]')
                l.clear()
                l.send_keys(str(housesNeeded))
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
                            if n.get_attribute("innerText")[:5] in "House":
                                oilUsed = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,f'//span[@class="imp small oil tip"]'))).get_attribute("textContent")
                                print(oilUsed)
                                oilData=oilUsed.split()
                                print(oilData)
                                if oilData[1]=="KK":
                                    oilQuantity= float(oilData[0])*10**6
                                elif oilData[1]=="KKK":
                                    oilQuantity= float(oilData[0])*10**9
                                oreUsed = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,f'//span[@class="imp ore small tip"]'))).get_attribute("textContent")
                                print(oreUsed)
                                oreData=oreUsed.split()
                                print(oreData)
                                if oreData[1]=="KK":
                                    oreQuantity= float(oreData[0])*10**6
                                elif oilData[1]=="KKK":
                                    oreQuantity= float(oreData[0])*10**9
                                moneyEquivalence = oilQuantity*140+oreQuantity*130
                                print(thousandsToK(moneyEquivalence))
                                try:
                                    n.click()
                                except:
                                    driver.execute_script("arguments[0].click();", n)
                                foundLaw = True
                                break
                    time.sleep(2)
                    if foundLaw:
                        driver.find_element(By.XPATH,'//div[@id="offer_show_v"]/div/div[@url="pro"]').click() # Click on pro on the law
                        message = f"{housesNeeded} houses were successfully built in {region}. Cost: {oilData[0]} {oilData[1]} bbl and {oreData[0]} {oreData[1]} kg ({thousandsToK(moneyEquivalence)}) "
                        sendTG (TOKEN, chat_id, message)
                except Exception as e:
                    message = f"There was a problem building houses in {region}. Please do it manually. Error: {e}"
                    sendTG (TOKEN, chat_id, message)
                    pass
            else:
                pass
            
    except Exception as e: 
        print("RIP")
        message = f"There was a problem with AutoHouseBuilder . Please do it manually. Traceback: {e}"
        sendTG (TOKEN, chat_id, message)
        pass




def thousandsToK(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'KK', 'KKK', 'T'][magnitude])
            


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
    sendTG (TOKEN, chat_id, message)

    driver.delete_all_cookies()
    time.sleep(5)
    driver.get("https://rivalregions.com")
    time.sleep(5)
    try:
        loginAccount(driver)
        time.sleep(5)
        goldRenew(driver, chat_id, TOKEN)
    except:
        print("Failed to re-login")
        try:
            driver.quit()
            driver.close()
            reboot()
        except:
            print("Failed to bounce back")
            pass


    #https://stackoverflow.com/questions/59130200/selenium-wait-until-element-is-present-visible-and-interactable/59130336#59130336

