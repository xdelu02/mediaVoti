from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dataInputUI import *

x = "ciao"
PATH = "./chromedriver88.0.4324.96.exe"
driver = webdriver.Chrome(PATH)
codicescuola = codScuola
username = user
password = passw

# prima pagina
driver.get("http://"+codicescuola+".scuolanext.info")
driver.maximize_window()

try:
    inputUsername = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    inputPassword = driver.find_element_by_id("password")
    inputUsername.send_keys(username)
    inputPassword.send_keys(password)
    inputPassword.send_keys(Keys.RETURN)
finally:
    pass

# seconda pagina
try:
    inputUsername = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "menu-servizialunno:vot"))
    ).click()
finally:
    pass


time.sleep(20)
driver.quit()
