from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
from twilio.rest import Client

# Sub-task 1: Enter username and password into textbox
def enter_credentials(username, password, textbox_selector):
    driver.find_element_by_css_selector(textbox_selector).send_keys(username)
    driver.find_element_by_css_selector(textbox_selector).send_keys(Keys.TAB)
    driver.find_element_by_css_selector(textbox_selector).send_keys(password)

# Sub-task 2: Click a specific button given the selector
def click_button(button_selector):
    driver.find_element_by_css_selector(button_selector).click()

# Sub-task 3: Screenshot the whole webpage and save it as .jpg
def take_screenshot(filename):
    pyautogui.screenshot(filename)

# Sub-task 4: Connect to WhatsApp API and send the .jpg to a specific group
def send_whatsapp_message(account_sid, auth_token, from_whatsapp_number, to_whatsapp_number, media_url):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="New screenshot!",
        from_=from_whatsapp_number,
        media_url=[media_url],
        to=to_whatsapp_number
    )
    print("WhatsApp message sent!")

# Set up the Selenium web driver
driver = webdriver.Chrome()  # Replace with the appropriate driver for your browser

# Sub-task 1: Enter username and password
username = "your_username"
password = "your_password"
textbox_selector = "your_textbox_selector"
enter_credentials(username, password, textbox_selector)

# Sub-task 2: Click a specific button
button_selector = "your_button_selector"
click_button(button_selector)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

# Sub-task 3: Screenshot the whole webpage and save it as .jpg
screenshot_filename = "screenshot.jpg"
take_screenshot(screenshot_filename)

# Sub-task 4: Connect to WhatsApp API and send the .jpg to a specific group
account_sid = "your_account_sid"
auth_token = "your_auth_token"
from_whatsapp_number = "your_from_whatsapp_number"
to_whatsapp_number = "your_to_whatsapp_number"
media_url = "file://" + screenshot_filename
send_whatsapp_message(account_sid, auth_token, from_whatsapp_number, to_whatsapp_number, media_url)

# Close the web driver
driver.quit()
