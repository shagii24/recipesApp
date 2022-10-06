#from selenium import webdriver
#set chromodriver.exe path
#driver = webdriver.Chrome(executable_path='C://Program Files//Google//Chrome//Application//chrome.exe')
#driver.implicitly_wait(0.5)
#launch URL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://sklep.pgg.pl/")




#driver.get("https://sklep.pgg.pl/")

import time

refresh_time_in_seconds = 15

url = driver.current_url
while(True):
    if url == driver.current_url:
        driver.refresh()
    url = driver.current_url
    time.sleep(refresh_time_in_seconds)