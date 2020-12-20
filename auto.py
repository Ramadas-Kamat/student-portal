from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import os.path
from os import path
import sqlite3
import schedule
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from dhooks import Webhook
#import discord_webhook
#email, password, webhooklink, orgname, timetable
def bot(email, password, webhooklink, orgname, timetable):
    opt = Options()
    opt.add_argument("--disable-infobars")
    opt.add_argument("start-maximized")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--start-maximized")
    # Pass the argument 1 to allow and 2 to block
    opt.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1, 
        "profile.default_content_setting_values.notifications": 1 
    })

    driver = None
    URL = "https://teams.microsoft.com"

    def start_browser():
        global driver
        PATH = "chrome/chromedriver.exe"
        driver = webdriver.Chrome(options=opt, executable_path=PATH)
        driver.get(URL)

        WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))

        if("login.microsoftonline.com" in driver.current_url):
            login()

    def login():
        global driver
        global hook
        #login required
        print("logging in")
        emailField = WebDriverWait(driver,20000).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="i0116"]')))
        emailField.click()
        emailField.send_keys(email)
        #time.sleep(5)
        #driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Next button
        WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="idSIButton9"]'))).click()
        #time.sleep(10)
        #passwordField = driver.find_element_by_xpath('//*[@id="i0118"]')
        passwordField = WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="i0118"]')))
        passwordField.click()
        #time.sleep(10)
        passwordField.send_keys(password)

        #driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Sign in button
        WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="idSIButton9"]'))).click()
        hook = Webhook(webhooklink)
        hook.send("Successfully logged in")

        #time.sleep(10)

        try:
            #driver.find_element_by_xpath('/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a').click()
            WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'/html/body/promote-desktop/div/div/div/div[1]/div[2]/div/a'))).click()	
            #time.sleep(10)
        except:
            pass
        
        try:
            #driver.find_element_by_class_name('guest-license-error-dropdown-title').click()
            WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.CLASS_NAME,'guest-license-error-dropdown-title'))).click()
            time.sleep(5)
            list_of_org = driver.find_elements_by_class_name('tenant-name')
            #list_of_org = WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.CLASS_NAME,'tenant-name')))
            for org in list_of_org:
                if org.text == orgname:#org_name
                    org.click()
                    break
            #driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/div[2]/div[4]/button').click()
            WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="page-content-wrapper"]/div[1]/div/div[2]/div[4]/button'))).click()
        except:
            pass

    def joinclass(class_name,start_time,end_time):
        global driver
        global hook
        try_time = int(start_time.split(":")[1]) + 15
        try_time = start_time.split(":")[0] + ":" + str(try_time)

        time.sleep(5)
        classes_available = driver.find_elements_by_class_name("name-channel-type")
        #classes_available = WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.CLASS_NAME,'name-channel-type')))

        for i in classes_available:
            if class_name.lower() in i.get_attribute('innerHTML').lower():
                print("JOINING CLASS ",class_name)
                i.click()
                break
        time.sleep(5)
        try:
            #joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
            joinbtn = WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.CLASS_NAME,'ts-calling-join-button')))
            joinbtn.click()

        except:
            #join button not found
            #refresh every minute until found
            k = 1
            while(k<=15):
                print("Join button not found, trying again")
                time.sleep(60)
                driver.refresh()
                joinclass(class_name,start_time,end_time)
                k+=1
            print("Seems like there is no class today.")
            #discord_webhook.send_msg(class_name=class_name,status="noclass",start_time=start_time,end_time=end_time)
            hook = Webhook(webhooklink)
            hook.send(f"Class: {class_name} has not started yet, itseems like class is cancelled")


        #time.sleep(5)
        #webcam = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
        webcam = WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')))
        if(webcam.get_attribute('title')=='Turn camera off'):
            webcam.click()
        #time.sleep(10)

        #microphone = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
        microphone = WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="preJoinAudioButton"]/div/button/span[1]')))
        if(microphone.get_attribute('title')=='Mute microphone'):
            microphone.click()

        #time.sleep(10)
        #joinnowbtn = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
        joinnowbtn = WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')))
        joinnowbtn.click()

        #discord_webhook.send_msg(class_name=class_name,status="joined",start_time=start_time,end_time=end_time)
        #hook = Webhook("https://discord.com/api/webhooks/788814336956301354/kA0EkFccceCOD21LgBAyD4Q_jWIjJN8K7rvmSD6BBLci_ltHxJvtPjedLIcNp5Diu_9C")
        now = datetime.now()

        current_time = now.strftime("%H:%M")
        hook = Webhook(webhooklink)
        hook.send("--------------------------------------------------")
        hook.send(f"Bot has joined class: {class_name} at {current_time}")
        
        #now schedule leaving class
        tmp = "%H:%M"

        class_running_time = datetime.strptime(end_time,tmp) - datetime.strptime(start_time,tmp)

        time.sleep(class_running_time.seconds)

        #driver.find_element_by_class_name("ts-calling-screen").click()
        WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.CLASS_NAME,'ts-calling-screen'))).click()



        #driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click() #come back to homepage
        WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="teams-app-bar"]/ul/li[3]'))).click()
        #time.sleep(5)

        
        WebDriverWait(driver,20000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="hangup-button"]'))).click()
        print("Class left")
        
        hook = Webhook(webhooklink)
        hook.send(f"Bot has left class: {class_name} at {end_time}")
        hook.send("--------------------------------------------------")

    for i in timetable:
        start_time = i.start_time
        end_time = i.end_time
        name = i.class_name
        day = i.day
            
        schedule.every().day.at(start_time).do(joinclass,name,start_time,end_time)
        print("Scheduled class '%s' on %s at %s"%(name,day,start_time))

    #Start browser
    #
    start_browser()
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(10)