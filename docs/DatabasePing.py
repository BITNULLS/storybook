import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def httpDatabaseConnection():
    
    ser = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=ser, chrome_options=chrome_options)

    browser.get(os.getenv("DB_PAGE"))
    sleep(3)

    username = browser.find_element(By.XPATH, '//*[@id="username"]')
    password = browser.find_element(By.XPATH, '//*[@id="password"]')
    username.send_keys(os.getenv("USERNAME"))
    password.send_keys(os.getenv("PASSWORD"))
    submit = browser.find_element(By.XPATH, '//*[@id="ui-id-5"]')
    submit.click()
    sleep(3)
    print('Entered Dashboard')

    browser.close()

httpDatabaseConnection()
