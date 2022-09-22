import asyncio
import os
from dotenv import load_dotenv
from MoE import resourceRenew
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import schedule
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
options.headless = True # Run without chrome ui 
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

if __name__ == '__main__':
    driver = uc.Chrome(options)
        # chromeVersion = ChromeDriverManager().install()
        # driver = webdriver.Chrome(chromeVersion, chrome_options=options)
    driver.get("https://rivalregions.com") # The website we want to go to

    time.sleep(3)
        #driver.get_screenshot_as_file("test.png")
    try:                        #Waits for cookie popup
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//form/input[@name="mail"]')))
    except Exception as e:
        print("Failed to initate",e)
        pass
    loginAccount(driver)
    status()

    schedule.every().day.at("20:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("20:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("21:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("21:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("22:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("22:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("23:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("23:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("00:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("00:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("01:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("01:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("02:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("02:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("03:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("03:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("04:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("05:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("06:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("07:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("08:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("10:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("12:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("14:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("16:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("18:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("19:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("19:50").do(resourceRenew, driver, "gol")

    schedule.every().day.at("20:01").do(resourceRenew, driver, "oil")
    schedule.every().day.at("00:02").do(resourceRenew, driver, "oil")
    schedule.every().day.at("04:02").do(resourceRenew, driver, "oil")
    schedule.every().day.at("08:02").do(resourceRenew, driver, "oil")
    schedule.every().day.at("12:02").do(resourceRenew, driver, "oil")
    schedule.every().day.at("16:02").do(resourceRenew, driver, "oil")

    schedule.every().day.at("12:05").do(resourceRenew, driver, "ura")
    schedule.every().day.at("06:10").do(resourceRenew, driver, "ura")
    schedule.every().day.at("13:05").do(resourceRenew, driver, "ore")
    schedule.every().day.at("14:05").do(resourceRenew, driver, "dia")
    schedule.every().day.at("20:10").do(resourceRenew, driver, "ura")


    async def my_task(): # Task to repeat every 30 seconds
        while True:
            schedule.run_pending() # Look if any resource should be reactivated
            await asyncio.sleep(30)
    asyncio.run(my_task())


