import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
#driver = webdriver.Chrome("C:/Users/killianwk.lun/Downloads/tools/selenium/chromedriver.exe")
link = "https://www.az128.com/rk/306je"
link_whatsapp = "https://web.whatsapp.com/"
driver.get(link)
time.sleep(5)
# class js-login-dialog
# name login
#TextFieldName = driver.find_element)By.
# name password
# class login-btn
checkinButton = driver.find_element(By.CLASS_NAME, "icon_past")
checkinButton.click()
time.sleep(10)
driver.close()