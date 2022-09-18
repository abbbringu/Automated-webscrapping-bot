from discord.ext import commands
import asyncio
import os
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from MoE import resourceRenew, deepExploraiton, status, reset
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import schedule
import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
from helper import loginAccount, check_exists_by_xpath
import pyperclip
load_dotenv()
import re
#--------------------------- Variable declaration ---------------------------- 
# Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
# Password = os.environ["account_password"]

# options = Options()
# options.add_argument("--disable-web-security")
# options.add_argument("--disable-site-isolation-trials")
# options.add_argument('--log-level=1')
# options.add_argument("--lang=en")
# options.headless = False # Run without chrome ui 
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.


    # driver = uc.Chrome(options)
    #     # chromeVersion = ChromeDriverManager().install()
    #     # driver = webdriver.Chrome(chromeVersion, chrome_options=options)
    # driver.get("https://rivalregions.com") # The website we want to go to

    # time.sleep(3)
    #     #driver.get_screenshot_as_file("test.png")
    # try:                        #Waits for cookie popup
    #     WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//form/input[@name="mail"]')))
    # except Exception as e:
    #     print("Failed to initate",e)
    #     pass
    # loginAccount(driver)
    # status()
def tax_bot(driver, day):
    time.sleep(2)
    print("test 0")
    driver.find_element(By.XPATH,'//div/span[@id="money"]').click()
    time.sleep(2)
    print("test 1")
    driver.find_element(By.XPATH,'//div/h1/span[@id="log_change"]').click()
    time.sleep(2)
    dates = driver.find_elements(By.XPATH,'//div[@id="timeline"]/div[@class="timeline_bottom"]/ul/li')
    time.sleep(1)
    print("test 2")
    dates[day].click()
    time.sleep(2)
    a = ActionChains(driver)
    a.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    time.sleep(1)
    print("test 3")
    a.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    time.sleep(1)
    s = pyperclip.paste()
    print("test 4")
    s = s.partition("Show")[0].split("\n",2)[2]

    return s
