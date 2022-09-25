rom discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from MoE import fuckzoco, resourceRenew, deepExploraiton, status, reset
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
import schedule
import undetected_chromedriver.v2 as uc
from dotenv import load_dotenv
import os
from helper import loginAccount
import Tax
import discord
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from xvfbwrapper import Xvfb
from app.hcaptcha import hCaptcha
from app.utils.colors import GREEN, RED, RESET
from app.utils.const import DEMONSTRATION_URL
vdisplay = Xvfb(width=800, height=1280)
vdisplay.start()

load_dotenv()
#--------------------------- Variable declaration ---------------------------- 
Mail =  os.environ["account_mail"]    #Fill your login info from env file os.environ["vonage_api"]
Password = os.environ["account_password"]

options = webdriver.ChromeOptions()
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
#options.add_argument("--headless")
options.headless = False
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=en")
options.add_argument('--log-level=1')
options.add_argument("--disable-site-isolation-trials")
options.add_argument("--disable-web-security")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-dev-shm-usage')
#ua = UserAgent()
#userAgent = ua.random
#print(userAgent)
#options.add_argument(f'user-agent={userAgent}')

def demonstration(hcaptcha: object) -> None:
    """Demonstration of the hCAPTCHA solver."""
    try:
        print('Solving the hCAPTCHA.', end=' ')
        hcaptcha.driver.get(DEMONSTRATION_URL)  # hCAPTCHA solver test URL.
        # Check if the lenght of "data-hcaptcha-response" attribute is
        # not null. If it's not null, the hCAPTCHA is solved.
        WebDriverWait(hcaptcha.driver, 600).until(lambda _: len(hcaptcha.visible(
            '//div[@class="h-captcha"]/iframe').get_attribute(
                'data-hcaptcha-response')) > 0)
        print(f'{GREEN}Solved.{RESET}')
    except TE:  # Something went wrong.
        print(f'{RED}Failed.{RESET}')
        
if __name__ == '__main__':
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = uc.Chrome(options=options, use_subprocess=True, service=chrome_service)
    #driver = uc.Chrome(options=options)
    driver.execute_script('return navigator.webdriver')
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.125 Safari/537.36'})
    driver.maximize_window()
    email = "yourmail@gmail.com"
    password = "your password"

    options = webdriver.ChromeOptions()
    #options.add_argument('proxy-server=106.122.8.54:3128')
    #options.add_argument(r'--user-data-dir=C:\Users\suppo\AppData\Local\Google\Chrome\User Data\Default')

    browser = uc.Chrome(
        options=options,
    )
    browser.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    browser.find_element(By.ID, 'identifierId').send_keys(email)

    browser.find_element(
        By.CSS_SELECTOR, '#identifierNext > div > button > span').click()

    password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

    browser.find_element(
        By.CSS_SELECTOR, password_selector).send_keys(password)
    
    browser.find_element(
        By.CSS_SELECTOR, '#passwordNext > div > button > span').click()
        # chromeVersion = ChromeDriverManager().install()
        # driver = webdriver.Chrome(chromeVersion, chrome_options=options)
    driver.get("https://rivalregions.com") # The website we want to go to
    hcaptcha = hCaptcha(  # Initialize the hCAPTCHA class.
        browser=1, headless=False, comments=True, download=False)
    hcaptcha.download_userscript()  # Download the userscript.
    demonstration(hcaptcha)  # Demonstrate the hCAPTCHA solver.


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
    schedule.every().day.at("21:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("22:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("23:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("00:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("01:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("02:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("03:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("04:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("05:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("06:30").do(resourceRenew, driver, "gol")
    schedule.every().day.at("08:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("10:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("12:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("14:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("16:00").do(resourceRenew, driver, "gol")
    schedule.every().day.at("18:00").do(resourceRenew, driver, "gol")

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

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='€',intents=intents)
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
        await ctx.send(f"Attemting to deep explore! :D Please wait a moment  {ctx.message.author.mention} <3")
        deepExploraiton(driver, location, resources.index(typeR.lower()), amount)
        await ctx.send("Done with the attempt, check if it was sucessful")

    @bot.command(name='renew', help='Make renew explorations. €renew <typ   e in 3 letters ex gol, oil, ura>')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def renew(ctx, typeR: str):
        if ((ctx.author == bot.user) or not(typeR in resources) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send(f"Attemting to renew explore! :D Please wait a moment {ctx.message.author.mention} <3")
        resourceRenew(driver, typeR)
        await ctx.send("Done with the attempt, check if it was sucessful")
    
    @bot.command(name='tax', help='Make renew explorations. €renew <typ   e in 3 letters ex gol, oil, ura>')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def tax(ctx, day: int):
        if ((ctx.author == bot.user) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send(f"Attemting to take tax! :D Please wait a moment {ctx.message.author.mention} <3")
        s = Tax.tax_bot(driver, day)
        await ctx.send(s)

    @bot.command(name='cancel', help='Cancels law')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def cancel(ctx):
        if ((ctx.author == bot.user) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send(f"Attemting to cancel law! :D Please wait a moment  {ctx.message.author.mention} <3")
        await ctx.send("This feature is not ready yet (￣y▽,￣)╭ ")

    @bot.command(name='info', help='info')
    async def info(ctx):
        if ((ctx.author == bot.user) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send(bot_info)

    @bot.command(name='fuckzoco', help='Renews resources in every region except Northern Ireland. Made with love by Turdetano :ratilla:. €fuckzoco <type in 3 letters ex gol, oil, ura>')
    @commands.has_any_role(discord_role, discord_role1, discord_role2)
    async def renew(ctx, typeR: str):
        if ((ctx.author == bot.user) or not(typeR in resources) or int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            await ctx.send("Error, either input error, or you are in the wrong channel")
            return
        await ctx.send(f"Attemting to fuck zoco! :D Please wait a moment {ctx.message.author.mention} <3")
        fuckzoco(driver, resources.index(typeR.lower()))
        await ctx.send("Done with the attempt, check if it was sucessful")

        

    @bot.event
    async def on_ready(): # When the bot is ready
        print('We have logged in as {0.user}'.format(bot))
        print("Initiated")

    @bot.event
    async def on_command_error(ctx, error): # Error handling
        if(int(ctx.channel.id) != int( os.environ["discord_channel_id"])):
            return
        await ctx.send(f"I''m not feeling good, 404, { error }")

    async def my_task(): # Task to repeat every 30 seconds
        while True:
            schedule.run_pending() # Look if any resource should be reactivated
            await asyncio.sleep(30)

    bot.run(TOKEN)

    async def my_task(): # Task to repeat every 30 seconds
        while True:
            schedule.run_pending() # Look if any resource should be reactivated
            await asyncio.sleep(30)
    asyncio.run(my_task())


