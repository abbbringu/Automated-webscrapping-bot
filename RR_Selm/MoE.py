# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.chrome.options import Options
import time
import datetime
import schedule
import undetected_chromedriver as uc
from dotenv import load_dotenv, set_key
import os

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
    #driver.get_screenshot_as_file("wow.png")

    #------------------------ Helper Function declarations ----------------------- 
    def check_exists_by_xpath(xpath):
        try:
            driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
    def loginAccount():        #Logs into facebook for rival regions. 1st step?
        print(driver.current_url)
        l=driver.find_element(By.XPATH,'//form/input[@name="mail"]') #Fills the user information then login
        l.send_keys(Mail)
        l=driver.find_element(By.XPATH,'//form/input[@name="p"]')
        l.send_keys(Password)
        time.sleep(1)
        l.send_keys(Keys.ENTER) #presses enter
        time.sleep(3)
    def goToParliament():           # From home screen, go to law section
        time.sleep(3)
        driver.find_element(By.XPATH,'//div[@action="parliament"]').click()  
    def select_law(int):
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
                accept_law()
            except:
                print("Failed to recoup")
            return

        try:                        #until we can click it
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(law[int])).click()
        except:
            print("Could not click, type law error")
            pass
    def state_exploration(resource_type):
        """ 
            0 = Gold
            1 = Oil
            2 = Ore
            3 = Uranium
            4 = Diamonds 
        """ 
        select_law(4) #go to resource law
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
    def accept_law():
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
        
    #------------------------------ Timed functions ------------------------------
    def resourceRenew(typeR="gol"):  #Code that executs after schedule 
        resources = ["gol", "oil", "ore", "ura", "dia"]
        ct = datetime.datetime.now()
        driver.get("https://rivalregions.com") # The website we want to go to
        time.sleep(3)
        print("Refilling ", typeR, ct)
        try:
            while True:
                goToParliament()
                if accept_law():
                    break
                state_exploration(resources.index(typeR))
                accept_law() 
                break
        except:
            reset(typeR)
    def deepExploraiton(locIndex, resource_index, amount):
        driver.get("https://rivalregions.com") # The website we want to go to
        try:
            while True:
                time.sleep(3)
                goToParliament()
                # driver.get_screenshot_as_file("test.png")
                if(driver.current_url == "https://rivalregions.com/#parliament"):
                    select_law(3)
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
                        accept_law()
                    except Exception as e:
                        print("Could not click, type resource error", e)
                        pass
                    break
        except: print("RIP")
    def status():
        ct = datetime.datetime.now()
        print("Alive", ct)
    def reset(typeR="default"): # type is where the code is comming from
        ct = datetime.datetime.now()    
        print("Doing a reset", ct)
        driver.delete_all_cookies()
        time.sleep(5)
        driver.get("https://rivalregions.com")
        time.sleep(5)
        try:
            loginAccount()
            time.sleep(5)
        except:
            print("Failed to re-login")
            pass
        try:
            if typeR == "gol":
                resourceRenew("gol")
            elif typeR == "oil":
                resourceRenew("oil")
            elif typeR == "ura":
                resourceRenew("ura")
        except:
            print("Failed to bounce back")
            pass
    
    #------------------------- Executed code Before loop--------------------------
    status()
    time.sleep(3)
    #driver.get_screenshot_as_file("test.png")
    try:                        #Waits for cookie popup
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//form/input[@name="mail"]')))
    except Exception as e:
        print("Failed to initate",e)
        pass
    loginAccount()

    #------------------------------ Time managment -------------------------------
    #schedule.every(2).hours.at(":02").do(gold) # Do gold every hour at 01 minutes
    schedule.every().day.at("20:00").do(resourceRenew, "gol")
    schedule.every().day.at("21:30").do(resourceRenew, "gol")
    schedule.every().day.at("23:00").do(resourceRenew, "gol")
    schedule.every().day.at("00:30").do(resourceRenew, "gol")
    schedule.every().day.at("02:00").do(resourceRenew, "gol")
    schedule.every().day.at("03:30").do(resourceRenew, "gol")
    schedule.every().day.at("05:00").do(resourceRenew, "gol")
    schedule.every().day.at("06:30").do(resourceRenew, "gol")
    schedule.every().day.at("08:00").do(resourceRenew, "gol")
    schedule.every().day.at("10:00").do(resourceRenew, "gol")
    schedule.every().day.at("12:00").do(resourceRenew, "gol")
    schedule.every().day.at("14:00").do(resourceRenew, "gol")
    schedule.every().day.at("16:00").do(resourceRenew, "gol")
    schedule.every().day.at("18:00").do(resourceRenew, "gol")
 
    schedule.every().day.at("20:01").do(resourceRenew, "oil")
    schedule.every().day.at("00:02").do(resourceRenew, "oil")
    schedule.every().day.at("04:02").do(resourceRenew, "oil")
    schedule.every().day.at("08:02").do(resourceRenew, "oil")
    schedule.every().day.at("12:02").do(resourceRenew, "oil")
    schedule.every().day.at("16:02").do(resourceRenew, "oil")

    schedule.every().day.at("12:05").do(resourceRenew, "ura")
    schedule.every().day.at("13:05").do(resourceRenew, "ore")
    schedule.every().day.at("14:05").do(resourceRenew, "dia")
    schedule.every().day.at("20:10").do(resourceRenew, "ura")
    
    #------------------------ Code loop and discord bot --------------------------
    from discord.ext import commands
    import asyncio

    TOKEN = os.environ["discord_bot_token"]
    discord_role = 'Lord-Treasurer 💰'
    discord_role1 = 'Treasurer 💰'
    discord_role2 = 628986324900249603
    bot_info= """
    Commands:
    €renew <resource>
    This will do a state exploration on the resource you choose
    
    €deep <location> <resource> <amount>
    This will do a deep exploration on the location you choose, with the resource, and the amount you choose. 

    €cancel
    This will make an attempt to cancel a law the bot is being stuck on. Currently not available

    ----------------------
    resource:
    you type the 3 first letters in the resource type - 
    Gold - gol
    Oil - oil
    Ore - ore
    Diamond - dia
    Uranium - ura

    location:
    Every region is represented by a nummber, that being from alphabetical order.
    Belfast - 0
    Cardiff - 1
    Channel Islands - 2
    Dublin - 3
    East Scotland - 4
    Edinburgh - 5
    Faroe Islands - 6
    Gibraltar - 7
    Highlands of Scotland - 8
    Iceland - 9
    Isle of Man - 10
    London - 11
    Midland and West Ireland - 12
    North East Scotland - 13
    North West England - 14
    Northern Ireland - 15
    Palau - 16
    South West England - 17
    South West Scotland - 18
    South and East Ireland - 19
    Swansea - 20

    """


    bot = commands.Bot(command_prefix='€')
    resources = ["gol", "oil", "ore", "ura", "dia"]
    @bot.command(name='deep', help='Make deep explorations. €deep <location number> <Type of resource> <amount>')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def deep(ctx, location: int, typeR: str, amount: int):
        if ctx.author == bot.user or int(ctx.channel.id) != int(os.environ["discord_channel_id"]):
            await ctx.send("Please do this in the right channel! <3")
            return
        elif (location > 20 or not(typeR.lower() in resources)):
            await ctx.send("Input seems to be wrong. Check again!")
            return
        await ctx.send("Attemting to deep explore! :D Please wait a moment <3")
        deepExploraiton(location, resources.index(typeR.lower()), amount)
        await ctx.send("Done with the attempt, check if it was sucessful")

    @bot.command(name='renew', help='Make renew explorations. €renew <typ   e in 3 letters ex gol, oil, ura>')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def renew(ctx, typeR: str):
        if ((ctx.author == bot.user) or not(typeR in resources) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send("Attemting to renew explore! :D Please wait a moment <3")
        resourceRenew(typeR)
        await ctx.send("Done with the attempt, check if it was sucessful")

    @bot.command(name='cancel', help='Cancels law')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def cancel(ctx):
        if ((ctx.author == bot.user) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send("Attemting to cancel law! :D Please wait a moment <3")
        await ctx.send("This feature is not ready yet (￣y▽,￣)╭ ")
    
    @bot.command(name='info', help='info')
    async def info(ctx):
        if ((ctx.author == bot.user) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send(bot_info)

        

    @bot.event
    async def on_ready(): # When the bot is ready
        print('We have logged in as {0.user}'.format(bot))
        print("Initiated")

    @bot.event
    async def on_command_error(ctx, error): # Error handling
        if(int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            return
        await ctx.send('I''m not feeling good, 404')

    async def my_task(): # Task to repeat every 30 seconds
        while True:
            schedule.run_pending() # Look if any resource should be reactivated
            await asyncio.sleep(30)

    bot.loop.create_task(my_task())
    bot.run(TOKEN)

                    