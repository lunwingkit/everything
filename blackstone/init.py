import io
import os
import shutil
from webbrowser import Chrome
import schedule
import time
import requests
from datetime import datetime
from PIL import ImageGrab, Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

HAVE_RED_POCKET_TODAY = False
GREEN_API_INSTANCE_ID = '7103839855'
GREEN_API_TOKEN_INSTANCE = 'e67d2fab892748498f9f612c443efe262e9b075381584406a4'
BLACKSTONE_GROUP_ID = "85255354152-1620457147@g.us" # "120363128913951312@g.us"
# TEST_GROUP_ID = "85255354152-1620457147@g.us"
# my Img group for testing purposes
TEST_PERSON_ID = ""
BLACKSTONE_PERSON_ID = "PERSON"

BLACKSTONE_VIDEO_URL = "https://www.az128.com/rk/306je"
BLACKSTONE_LOGIN_USERNAME = "601720"
BLACKSTONE_LOGIN_PASSWORD = "4152"

VIDEO_CHECKIN_PIC_DIRECTORY = 'D:/workspace/everything/blackstone/res'
VIDEO_CHECKIN_PIC_PATH = VIDEO_CHECKIN_PIC_DIRECTORY + '/test.jpg'
VIDEO_CHECKIN_PIC_LAKE_DIRECTORY = VIDEO_CHECKIN_PIC_DIRECTORY + '/backups/'

XPATH_LOGIN_BUTTON = ''
XPATH_USERNAME_TEXTBOX = ''
XPATH_PASSWORD_TEXTBOX = ''
XPATH_CHECKIN_BUTTON = ''
XPATH_VIDEO_PLAY_BUTTON = '' #maybe its
driver: webdriver.Chrome = None

def openUrl():
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome("C:/Users/killianwk.lun/Downloads/tools/selenium/chromedriver.exe")
    driver.set_window_size(375,812)
    driver.get(BLACKSTONE_VIDEO_URL)

def loginBlackStone():
    global driver
    try:
        driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON).click()
        driver.find_element(By.XPATH, XPATH_USERNAME_TEXTBOX).send_keys(BLACKSTONE_LOGIN_USERNAME)
        driver.find_element(By.XPATH, XPATH_PASSWORD_TEXTBOX).send_keys(BLACKSTONE_LOGIN_PASSWORD)
        driver.find_element(By.XPATH, XPATH_USERNAME_TEXTBOX).send_keys(Keys.ENTER)
    except Exception as e:
        raise Exception("Unable to login")

def playVideo():
    global driver
    try:
        driver.find_element(By.XPATH, XPATH_VIDEO_PLAY_BUTTON).click()
    except Exception as e:
        raise Exception("Unable to play video")

def checkinBlackStone():
    global driver
    try:
        driver.find_element(By.XPATH, XPATH_CHECKIN_BUTTON).click()
    except Exception as e:
        raise Exception("Unable to checkin")

def getRedPocketBlackStone():
    print("Get RedPocket Black")

def sendWhatsappMessage(recepients, message):
    url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE_ID}/sendMessage/{GREEN_API_TOKEN_INSTANCE}"
    payload = "{\r\n\t\"chatId\": \"" + recepients + "\",\r\n\t\"message\": \"" + message + "\"\r\n}"
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, data = payload.encode('utf-8'))
    print(response.text)
    print(datetime.now().strftime("%H:%M:%S") + " send[" + message + "] to " + str(recepients))
    return response

def sendWhatsappMessageWithFile(recepients, filename):
    url = f"https://api.green-api.com/waInstance{GREEN_API_INSTANCE_ID}/sendFileByUpload/{GREEN_API_TOKEN_INSTANCE}"
    payload = {
        'chatId': recepients,
        'caption': ''
        }
    files = [('file', ('cap_screen.jpeg', open(filename, 'rb'),'image/jpeg'))]
    headers= {}
    response = requests.request("POST", url, headers = headers, data = payload, files = files)
    print(response.text)

def capScreenAndSendtoGroup():
    openUrl()
    loginBlackStone()
    playVideo()
    #checkinBlackStone()

    screenCapSaveAsJPG()
    #sendWhatsappMessageWithFile(BLACKSTONE_GROUP_ID, VIDEO_CHECKIN_PIC_PATH)
    backupScreenCapPic()    
    while datetime.now().time().hour < 22:
        print("current time before 10 pm" + str(datetime.now().time()))
        time.sleep(5)
    print("After 10pm")

def screenCapSaveAsJPG():
    scrrenshot = driver.get_screenshot_as_png()
    pil_image = Image.open(io.BytesIO(scrrenshot))
    pil_image = pil_image.convert('RGB')
    pil_image.save(VIDEO_CHECKIN_PIC_PATH, 'JPEG')

def backupScreenCapPic():
    filename = "backup-" + datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    destination_path = VIDEO_CHECKIN_PIC_LAKE_DIRECTORY + filename
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.move(VIDEO_CHECKIN_PIC_PATH, destination_path)

def checkinWhatsappTask():
    response = sendWhatsappMessage(BLACKSTONE_GROUP_ID, "簽到")
    print("HELPER" + response.status_code)
    if response.status_code != 200:
        raise Exception("Message could not be sent")
    

def watchLivestreamVideoTask():
    openUrl()
    
    capScreenPng = checkinBlackStone()
    sendWhatsappMessage(BLACKSTONE_GROUP_ID, capScreenPng)

    if HAVE_RED_POCKET_TODAY:
        capScreenPng = getRedPocketBlackStone()
        sendWhatsappMessage(BLACKSTONE_PERSON_ID, capScreenPng)
    #do leave the video playing until 10pm
    

# Schedule the job to run every day at 9 PM
# try:
#     schedule.every().day.at("19:39").do(checkinWhatsappTask)
#     schedule.every().day.at("21:00").do(watchLivestreamVideoTask)
# except Exception as e:
#     print(e)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

capScreenAndSendtoGroup()