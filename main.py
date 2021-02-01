from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import dataInputUI

PATH = ".\chromedriver88.0.4324.96" # "E:\GoogleDriver\chromedriver.exe"
driver = webdriver.Chrome(PATH)
codicescuola = dataInputUI.codScuola # sg18309
username = dataInputUI.user
password = dataInputUI.passw

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
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "menu-servizialunno:vot"))
    ).click()
finally:
    pass

# terza pagina (Voti)
try:
    divVoti = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "sheet-sezioneDidargo:panel-votiGiornalieri:pannello"))
    )
    voti = divVoti.find_elements_by_tag_name("fieldset")
    for voto in voti:
        materia = voto.find_element_by_tag_name("legend")
        print(materia.text)
        risultati = voto.find_elements_by_tag_name("tr")
        for risultato in risultati:
            try:
                res = risultato.find_element_by_tag_name("span")
            except:
                res = risultato.find_element_by_tag_name("div")
            finally:
                print(res.text)
finally:
    pass


time.sleep(20)
input()
driver.quit()
