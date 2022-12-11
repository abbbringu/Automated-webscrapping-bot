from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    
import time
from dotenv import load_dotenv
import datetime
import os
import requests
import traceback

load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]
#------------------------ Helper Function declarations ----------------------- 
def check_exists_by_xpath(driver,xpath):
    try:
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH,xpath)
        return True
    except NoSuchElementException:
        return False
def loginAccount(driver):        #Logs into facebook for rival regions. 1st step?
    print(driver.current_url)
    l=driver.find_element(By.XPATH,'//form/input[@name="mail"]') #Fills the user information then login
    l.send_keys(Mail)
    l=driver.find_element(By.XPATH,'//form/input[@name="p"]')
    l.send_keys(Password)
    time.sleep(1)
    l.send_keys(Keys.ENTER) #presses enter
    time.sleep(3)
def FBLogin(driver,chat_id,TOKEN, Mail):
    try:                       
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sa_sn imp float_left']"))).click()
        message = f"FB Login was carried out succesfully for {Mail}."
        sendTG (TOKEN, chat_id, message)
        
    except Exception as e:
        message = f"Unsuccesful trial to login with FB for {Mail}. Traceback: {e}"
        sendTG (TOKEN, chat_id, message)

def sendTG (TOKEN, chat_id, message):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(telegram_url).json())

def goToParliament(driver):           # From home screen, go to law section
    time.sleep(3)
    try:
        driver.find_element(By.XPATH,'//div[@action="parliament"]').click()
    except:
        driver.get("https://rivalregions.com/#parliament")
        driver.refresh()
        driver.implicitly_wait(5)

def select_law(driver, int):
    """
    0 = New Buildings 
    1 = Resource exploration
    2 = Military agreement
    3 = Deep exploration
    4 = Resource exploration state
    5 = War declarion     
    6 = Sea war declarion     
    Further may cause error due to not showing on scrren 
    """
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@action="parliament/offer"]'))).click()
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="offer_dd"]'))).click()
        time.sleep(5)
        law = driver.find_elements(By.XPATH,'//div[@id="offer_dd"]/ul/li')  #Get list on dropdown law list
    except:
        print("Error during law selection, cancelling law and running the script from start")
        try:
            driver.find_element(By.XPATH,'//div[@class="button_red par_new_law cancel_law"]').click()
            time.sleep(5)
        except:
            print("Failed to recoup")
            driver.delete_all_cookies()
            time.sleep(5)
            driver.get("https://rivalregions.com")
            time.sleep(5)
            try:
                loginAccount(driver)
                time.sleep(5)
            except:
                print("Failed to re-login")
                try:
                    driver.quit()
                    driver.close()
                    reboot()
                except:
                    print("Failed to bounce back")
                    pass
        return
    try:                        #until we can click it
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(law[int])).click()
    except:
        print("Could not click, type law error")
        pass
def state_exploration(driver, resource_type):
    """ 
        0 = Gold
        1 = Oil
        2 = Ore
        3 = Uranium
        4 = Diamonds 
    """ 
    select_law(driver,4) #go to resource law
    time.sleep(3)
    driver.find_element(By.XPATH,'//div[@url="42"]/div/div/div/div').click() # Click on dropdown list
    resource = driver.find_elements(By.XPATH,'//div[@url="42"]/div/div/ul/li') #Get list on dropdown resource list
    try:                        #Waits for element is clickable
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(resource[resource_type])).click() # try to click on the resource
    except:
        print("Could not click, type resource error")
        pass
    time.sleep(3)
    
    driver.find_element(By.XPATH,'//div[@id="offer_do"]').click() # Clicking on offer law
    
    time.sleep(3)
def gold_exploration(driver):
    """ 
        0 = Gold
        1 = Oil
        2 = Ore
        3 = Uranium
        4 = Diamonds 
    """ 
    select_law(driver,4) #go to resource law
    time.sleep(3)
    #driver.find_element(By.XPATH,'//div[@url="42"]/div/div/div/div').click() # Click on dropdown list
    #time.sleep(3)
    driver.find_element(By.XPATH,'//div[@id="offer_do"]').click() # Clicking on offer law
    time.sleep(3)
def accept_law(driver):
    foundLaw = False
    accept_laws=["Resources explor", "Deep exploration"]
    laws = driver.find_elements(By.XPATH,'//div[@id="parliament_active_laws"]/div/div/div') # Get all active laws
    for n in laws:  # Find which is Resources exploration
        if len(n.get_attribute("innerText")) > 20:
            if n.get_attribute("innerText")[0:16] in accept_laws:
                n.click()
                foundLaw = True
                break
    time.sleep(2)
    if foundLaw:
        driver.find_element(By.XPATH,'//div[@id="offer_show_v"]/div/div[@url="pro"]').click() # Click on pro on the law
    return foundLaw

def newMessageChecker (driver,chat_id, TOKEN, Mail):
    if check_exists_by_xpath(driver,"//div[@class='tip header_menu_item tc green_bg']")==True:
        message =f"A new message was received for {Mail}"
        sendTG(TOKEN,chat_id,message)
    else:
        print("No new messages")

def autoperk(driver,worksheet): #IN THE FUTURE/WONT DO
    if check_exists_by_xpath(driver,"//div[@class='no_imp hasCountdown']")==False:
        perkOptions = worksheet.get_row(4, include_tailing_empty=False)

    
    print("o")

def build_academy(driver,chat_id, TOKEN, Mail,worksheet): #COMPLETED
    lastBuilt = worksheet.get_row(5, include_tailing_empty=False)
    print(f"Last {lastBuilt[0]} built on the day {lastBuilt[1]} at {lastBuilt[2]} h for {Mail} ")
    if (lastBuilt [1] != str(datetime.date.today().isoweekday()) and int(datetime.datetime.now().hour) >= 19) or (int(lastBuilt[2])<19 and int(datetime.datetime.now().hour) >= 19 and lastBuilt[1]==str(datetime.date.today().isoweekday())):
        driver.get("https://rivalregions.com")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tip hov pointer quest_have_perk_ma']"))).click()
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green index_ma_quest']"))).click()
        time.sleep(3)
        if check_exists_by_xpath(driver,"//div[@class='button_green button_academy']")==True:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green button_academy']"))).click()
            lastBuilt[2] = str(datetime.datetime.now().hour)
            lastBuilt [1]= str(datetime.date.today().isoweekday())
            worksheet.update_row(5, lastBuilt, col_offset=0)
            message= f"Military academy is being built for {Mail}"
        elif check_exists_by_xpath(driver,"//div[@class='button_white']")==True:
            if check_exists_by_xpath(driver,"//span[@class='count_ma']")==True:
                print("Trying to move to residence region to build MA")
                try:
                    rr_id = lastBuilt[3]
                except IndexError:
                    lastBuilt.append(str(driver.get_cookie('rr_id')["value"]))
                    worksheet.update_value('D5', lastBuilt[3])
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header_buttons_hover_close']"))).click()
                driver.implicitly_wait(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[@action='slide/profile/{lastBuilt[3]}']"))).click()
                driver.implicitly_wait(3)
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tip header_buttons_hover slide_profile_link tc']"))).click()
                except:
                    click = driver.find_element(By.XPATH,"//div[@class='tip header_buttons_hover slide_profile_link tc']") 
                    driver.execute_script("arguments[0].click();", click)
                driver.implicitly_wait(3)
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green region_details_move']"))).click()
                except:
                    element = driver.find_element(By.XPATH,"//div[@class='button_green region_details_move']") 
                    driver.execute_script("arguments[0].click();", element)
                driver.implicitly_wait(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_blue map_d_b imp']"))).click()
                travelTime = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//span[@class="type_distance"]'))).get_attribute("textContent")
                travelTimeTable = travelTime.split(":")
                message= f"Arriving at residence in {travelTime} for {Mail}. {travelTimeTable}"
                travelTimeSeconds = str(int(travelTimeTable[0])*60+ int(travelTimeTable[1]))
                worksheet.update_value('B8', str(travelTimeSeconds))
                driver.implicitly_wait(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green map_d_b']"))).click()
            else:
                lastBuilt[2] = str(datetime.datetime.now().hour)
                lastBuilt[1]=str(datetime.date.today().isoweekday())
                worksheet.update_row(5, lastBuilt, col_offset=0)
                message= f"Military Academy was already built for {Mail}"
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header_buttons_hover_close']"))).click()
        else:
            message= f"An error was encountered while building Military Academy for {Mail}"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='header_buttons_hover_close']"))).click()
        sendTG (TOKEN, chat_id, message)
    else:
        print("Already built according to ProfileVariables")

def build_departments(driver,chat_id, TOKEN, Mail,worksheet): #COMPLETED
    lastBuilt = worksheet.get_row(6, include_tailing_empty=False)
    print(f"Last {lastBuilt[0]} built on the day {lastBuilt[1]} at {lastBuilt[2]} h for {Mail} ") #it's coded to run after 21 to prevent clogging at 19 and 20
    if (lastBuilt [1] != str(datetime.date.today().isoweekday()) and int(datetime.datetime.now().hour) >= 21) or (int(lastBuilt[2])<19 and int(datetime.datetime.now().hour) >= 19 and lastBuilt[1]==str(datetime.date.today().isoweekday())):
        listofdepartments=["buildings", "gold", "oil", "ore", "diamonds","uranium","liquidoxygen","helium-3","tanks","spacestations","battleships"]
        pointsfordepartments = worksheet.get_row(2, include_tailing_empty=False)
        driver.get("https://rivalregions.com/#state/details/3046/in")
        driver.refresh()
        time.sleep(3)
        driver.implicitly_wait(5)
        if check_exists_by_xpath(driver,"//div[@class='float_left button_green inst_do']")==True:
            for department in listofdepartments:
                print(department)
                points= int(pointsfordepartments[int(listofdepartments.index(str(department)))])
                print(str(points))
                url = int(int(listofdepartments.index(str(department)) +1))
                while points>0:
                    points = points-1
                    print(points)
                    element = driver.find_element("xpath", f"//div[@url='{url}'][@class='float_left hov2 pointer inst_plus green']") #find element and scroll down in case it is needed
                    element.location_once_scrolled_into_view
                    time.sleep(1)
                    try:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[@url='{url}'][@class='float_left hov2 pointer inst_plus green']"))).click()
                    except:
                        click = driver.find_element(By.XPATH,"//div[@class='float_left button_green inst_do']") 
                        driver.execute_script("arguments[0].click();", click)
                    driver.implicitly_wait(0.5)
                    print ("Clicking " + str(department))
            else:
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='float_left button_green inst_do']"))).click()
                except:
                    click = driver.find_element(By.XPATH,"//div[@class='float_left button_green inst_do']") 
                    driver.execute_script("arguments[0].click();", click)
                driver.implicitly_wait(1)
                time.sleep(1)
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='header_buttons_hover_close']"))).click()
                except:
                    click = driver.find_element(By.XPATH,"//div[@class='header_buttons_hover_close']") 
                    driver.execute_script("arguments[0].click();", click)
                time.sleep(1)
                lastBuilt[2] = str(datetime.datetime.now().hour)
                lastBuilt[1]=str(datetime.date.today().isoweekday())
                worksheet.update_row(6, lastBuilt, col_offset=0)
                message = f"Departments were built successfully for {Mail}"
                sendTG (TOKEN, chat_id, message)
                time.sleep(3)
        else:
            time.sleep(3)
            print("Departments were already built")
            driver.get("https://rivalregions.com/")
            driver.refresh()
            lastBuilt[2] = str(datetime.datetime.now().hour)
            lastBuilt[1]= str(datetime.date.today().isoweekday())
            worksheet.update_row(6, lastBuilt, col_offset=0)
    else:
        print("Already built according to ProfileVariables")


def military_training(driver, chat_id, TOKEN, Mail): #COMPLETED
    autoTraining = 0
    driver.get("https://rivalregions.com")
    driver.refresh()
    time.sleep(5)
    if check_exists_by_xpath(driver,"//span[@class='pointer hov2 dot'][contains(text(),'auto')]")==True:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='pointer hov2 dot'][contains(text(),'auto')]"))).click()
        if check_exists_by_xpath(driver,"//div[@class='tip button_green war_w_move']")==True:
            autoTraining= 2 
            print('Training is engaged in the wrong region')
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='slide_close']"))).click() #close autotab
            except:
                close = driver.find_element(By.XPATH,"//div[@id='slide_close']") 
                driver.execute_script("arguments[0].click();", close)
        else:
            print("Everything is right with AutoTraining")
    else:
        autoTraining = 1
        print("No training found")
    if autoTraining != 0:
        driver.implicitly_wait(3)
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='pointer index_training hov2 dot']"))).click() #go to training tab
        except:
            element = driver.find_element(By.XPATH,"//span[@class='pointer index_training hov2 dot']") 
            driver.execute_script("arguments[0].click();", element)
        if autoTraining ==2: #cancels training
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_red war_w_auto_cancel']"))).click() #cancels wrong training
            except:
                close = driver.find_element(By.XPATH,"//div[@class='button_red war_w_auto_cancel']") 
                driver.execute_script("arguments[0].click();", close)
        driver.implicitly_wait(1)
        if check_exists_by_xpath(driver,"//div[@class='tip button_green hide_for_guide war_w_auto_wd']")==True: #enables training
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tip button_green hide_for_guide war_w_auto_wd']"))).click()
            except:
                element = driver.find_element(By.XPATH,"//div[@class='tip button_green hide_for_guide war_w_auto_wd']") 
                driver.execute_script("arguments[0].click();", element)
            time.sleep(3)
            if check_exists_by_xpath(driver,"//div[@class='tip button_green hide_for_guide war_w_auto_wd']")==True: #if the button is still there, training was not started
                message = f"Tranining could not be resumed for {Mail}"
            else:
                message = f"Training continued for {Mail}"
            sendTG (TOKEN, chat_id, message)
        else:
            print("Already with auto (inside check)")
        print("AutoTraining is being set")
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='slide_close']"))).click()
    except:
        close = driver.find_element(By.XPATH,"//div[@id='slide_close']") 
        driver.execute_script("arguments[0].click();", close)

def autowork(driver,chat_id,TOKEN, Mail,worksheet): #IN THE WORKS: DESIRED FACTORY
    desiredFactoryList = worksheet.get_row(7, include_tailing_empty=False)
    driver.implicitly_wait(1)
    try:
        element = driver.find_element(By.XPATH,"//div[@class='item_menu work_menu ajax_action header_menu_item tc'][@action='work']") #site headers can only be clicked this way
        driver.execute_script("arguments[0].click();", element)
    except:
        driver.get("https://rivalregions.com/#work")
        driver.refresh()
    driver.implicitly_wait(1)
    autosell(driver, chat_id, TOKEN, Mail)
    if driver.current_url != "https://rivalregions.com/#work":
        driver.get("https://rivalregions.com/#work")
        driver.refresh()
        time.sleep(3)
    if check_exists_by_xpath(driver,"//div[@class='work_factory_button button_blue'][@reslittle='0']")==True or check_exists_by_xpath(driver,"//div[@class='button_white tip'][@reslittle='0']")==True or check_exists_by_xpath(driver,"//div[@class='tip button_white no_pointer']")==True:
        if check_exists_by_xpath(driver,"//div[@class='work_factory_button button_blue'][@reslittle='0']")==True or check_exists_by_xpath(driver,"//div[@class='button_white tip'][@reslittle='0']")==True:
            print("Your resource is depleted")
            reason = "the resource you worked has depleted in this region"
        elif check_exists_by_xpath(driver,"//div[@class='tip button_white no_pointer']")==True:
            print("You cannot work in your actual factory since you are in a wrong location")
            reason = "the region is wrong"
            #future option: check on a file where to fly (can be improved). if no place -> select factory with most workers (not done)
        nextFactory=False
        for desiredFactory in desiredFactoryList:
            print(str(desiredFactory))
            if desiredFactory=="Attack":
                print("Trying to attack")
                driver.get("https://rivalregions.com")
                driver.refresh()
                time.sleep(5)
                actionsXPATHList = ["//span[@class='pointer hov2 dot'][contains(text(),'auto')]","//div[@class='button_green war_w_send_ok']",
                "//div[@class='button_green war_w_send_ok']","//div[@id='header_my_fill_bar']",  "//div[@class='button_green war_w_send_ok']"]
                for XPATHaction in actionsXPATHList:
                    driver.implicitly_wait(5)
                    try:    
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, XPATHaction))).click()
                    except:
                        try:
                            tryAction = driver.find_element(By.XPATH,XPATHaction) #site headers can only be clicked this way
                            driver.execute_script("arguments[0].click();", tryAction)
                        except:
                            print("Not possible")
                message = f"Attacking for {Mail}"
                break
            driver.get(f'{desiredFactory}')
            driver.refresh()
            driver.implicitly_wait(1)
            if check_exists_by_xpath(driver,"//div[@class='factory_join_2 button_green']")== True:
                driver.implicitly_wait(3)
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='factory_join_2 button_green']"))).click()
                except:
                    click = driver.find_element(By.XPATH,"//div[@class='factory_join_2 button_green']") 
                    driver.execute_script("arguments[0].click();", click)
                driver.implicitly_wait(3)
                message = f"A new factory was selected as factory to work and running again Autowork for {Mail}"
                driver.get("https://rivalregions.com/#work")
                driver.refresh()
                time.sleep(3)
                break
            elif nextFactory == True:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='factory_whose']"))).click()
                driver.implicitly_wait(3)
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green region_details_move']"))).click()
                except:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='factory_whose']"))).click()
                    driver.reload()
                    time.sleep(3)
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green region_details_move']"))).click()
                driver.implicitly_wait(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_blue map_d_b imp']"))).click()
                travelTime = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//span[@class="type_distance"]'))).get_attribute("textContent")
                message= f"Arriving at {desiredFactory[8:]} in {travelTime} for {Mail}"
                travelTime = travelTime.split(":")
                travelTimeSeconds = str(int(int(travelTime[0])*60+ int(travelTime[1])))
                print(travelTimeSeconds+" s")
                worksheet.update_value('B8', str(travelTimeSeconds))
                driver.implicitly_wait(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green map_d_b']"))).click()
                break

            elif check_exists_by_xpath(driver,'//div[@class="factory_join_1 button_red"]')==True:
                print("Next factory")
                nextFactory = True
            else:
                message = f"Please check AutoWork for {Mail}, because {reason} and there are no instructions in the ProfileVariables"
        sendTG (TOKEN, chat_id, message)
    

    if check_exists_by_xpath(driver,"//div[@class='work_factory_button button_blue']")==True or check_exists_by_xpath(driver,"//div[@class='button_white tip']")==True:
        print("You are already bound to a factory here") #the line above checks: if you have energy and you can work or if you have no energy but you can work (only for gold mine)
        if check_exists_by_xpath(driver,"//div[@class='button_red cancel_auto_work']")==True: #if you cancel autowork, it checks how much time is left 
            timeLeft = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//span[@class="work_auto_countdown hasCountdown"]'))).get_attribute("textContent")
            print((timeLeft))
            print(timeLeft[0:2])
            if int(timeLeft[0:2]) < 5:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_red cancel_auto_work']"))).click()
                driver.implicitly_wait(5)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='work_w_autom button_red tip']"))).click()
                message = f"Autowork was cancelled and restarted for {Mail}"
                sendTG (TOKEN, chat_id, message)
        elif check_exists_by_xpath(driver,"//div[@class='work_w_autom button_red tip']")==True: #if you dont have auto enabled, it enables it
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='work_w_autom button_red tip']"))).click()
            driver.refresh()
            time.sleep(5)
            if check_exists_by_xpath(driver,"//div[@class='work_w_autom button_red tip']")==True:
                message = f"Something is wrong, please check AutoWork for {Mail}"
            else:
                message = f"AutoWork was enabled for {Mail}"
            sendTG (TOKEN, chat_id, message)
    time.sleep(3)



def autosell(driver, chat_id, TOKEN, Mail): #COMPLETED FOR NOW: SELLS AUTOMATICALLY WITH REFERENCE TO THE ACTUAL MARKET IF YOU WORK RESOURCE
    if driver.current_url != "https://rivalregions.com/#work":
        driver.get("https://rivalregions.com/#work")
        driver.refresh()
        time.sleep(3)
    resourceIndex= int((WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//img[@class="work_source_3 float_left"]'))).get_attribute("src"))[64:65])
    print(resourceIndex)
    indexToUrl= [None,None,"3","4","11","15","21","24","26" ]
    resourceUrl= indexToUrl[int(resourceIndex)]
    print(resourceUrl)
    indexToName = [None, "Gold", "Oil", "Ore", "Uranium", "Diamonds", "Liquid Oxygen", "Helium-3", "Rivalium"]
    resourceName= indexToName[int(resourceIndex)]
    if resourceUrl != None:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='item_menu storage_menu ajax_action header_menu_item tc']"))).click()
        time.sleep(3)
        driver.implicitly_wait(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='tip float_left white imp storage_item pointer hov ib_border'][@url='{resourceUrl}']"))).click()
        actualMarketPrice = int(''.join(filter(str.isdigit, WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//span[@class="storage_see pointer tip hov2 imp"]//span[@class="dot"]'))).get_attribute("textContent"))))
        print("The actual price in the market is "+str(actualMarketPrice))
        optimalSellPrice = int(round(actualMarketPrice*1.05))
        print(f"The optimal sell price is {optimalSellPrice} €")
        sellStatus = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//span[@class="storage_sell dot"]'))).get_attribute("textContent")
        print(sellStatus)
        if sellStatus == "edit your offer":
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='storage_sell dot']"))).click()
            try:
                oldSellPrice= int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//input[@class="storage_sell_price float_left imp white tpbg"]'))).get_attribute("value"))
            except:
                driver.reload()
                time.sleep(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='storage_sell dot']"))).click()
                oldSellPrice= int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//input[@class="storage_sell_price float_left imp white tpbg"]'))).get_attribute("value"))
            print(f"Our actual sell price is {oldSellPrice} €")
            if int(round(oldSellPrice*99/100))> optimalSellPrice:
                sellPrice= optimalSellPrice
            else:
                sellPrice = int(round(oldSellPrice*99/100))
            message = f"Our offer of {resourceName} was changed lowered from {oldSellPrice} € to {sellPrice} € for {Mail}"
        elif sellStatus == "place an offer":
            message = f"Selling {resourceName} for {optimalSellPrice} € for {Mail}"
            sellPrice = optimalSellPrice

        priceBox= WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//input[@class="storage_sell_price float_left imp white tpbg"]')))
        priceBox.clear()
        priceBox.send_keys(sellPrice)
        if sellStatus == "place an offer":
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_red storage_sell_button no_pointer']"))).click()
        elif sellStatus == "edit your offer":
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='button_green storage_sell_button']"))).click()
        sendTG (TOKEN, chat_id, message)

def repeatProcess(driver, chat_id, TOKEN, Mail,worksheet):
    repeatProcessTime = worksheet.get_value("B8")
    if repeatProcessTime != "":
        time.sleep(int(repeatProcessTime)+5)
        military_training(driver, chat_id, TOKEN, Mail)
        autowork(driver, chat_id, TOKEN, Mail,worksheet)
        worksheet.update_value('B8', '')




def autoProfile (driver, chat_id, TOKEN, Mail,worksheet):
    for profileVariableNumber in range (6):
        try:
            if profileVariableNumber==0:
                autoProfileTool = "RR Message Checker"
                newMessageChecker(driver, chat_id, TOKEN, Mail)
            elif profileVariableNumber==1:
                autoProfileTool = "Academy AutoBuilder"
                build_academy(driver, chat_id, TOKEN, Mail,worksheet)
            elif profileVariableNumber==2:
                autoProfileTool = "Department AutoBuilder"
                build_departments(driver,chat_id, TOKEN,Mail,worksheet)
            elif profileVariableNumber==3:
                autoProfileTool = "AutoTraining"
                military_training(driver, chat_id, TOKEN, Mail)
            elif profileVariableNumber==4:
                autoProfileTool = "AutoWork"
                autowork(driver, chat_id, TOKEN, Mail,worksheet)
            elif profileVariableNumber==5:
                autoProfileTool = "Repeat Process"
                repeatProcess(driver, chat_id, TOKEN, Mail,worksheet)

        except Exception as e:
            message = f"Error while running {autoProfileTool} for {Mail}. Exception: {e}. Traceback: {traceback.format_exc}"
            sendTG (TOKEN, chat_id, message)


def reboot():
    os.system("cd /home/gonzalo/RR/Programas/Turdetano && /home/gonzalo/RR/Programas/Turdetano/venv/bin/python3 /home/gonzalo/RR/Programas/Turdetano/main_dumb_firefox.py")


 


