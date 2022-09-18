from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    
import time
from dotenv import load_dotenv
import os    
load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]
#------------------------ Helper Function declarations ----------------------- 
def check_exists_by_xpath(driver,xpath):
    try:
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
def goToParliament(driver):           # From home screen, go to law section
    time.sleep(3)
    driver.find_element(By.XPATH,'//div[@action="parliament"]').click()  
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
        driver.find_element(By.XPATH,'//div[@action="parliament/offer"]').click()
        time.sleep(3)
        driver.find_element(By.XPATH,'//div[@id="offer_dd"]').click() # Click on dropdown list
        time.sleep(2)
        law = driver.find_elements(By.XPATH,'//div[@id="offer_dd"]/ul/li')  #Get list on dropdown law list
    except:
        print("error during law selection")
        try:
            accept_law(driver)
        except:
            print("Failed to recoup")
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
