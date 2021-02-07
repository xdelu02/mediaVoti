from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import dataInputUI
import re
from datetime import datetime

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
mediaPrimoQuad = 0.0
nVotiPrimoQuad = 0.0
mediaSecondoQuad = 0.0
nVotiSecondoQuad = 0.0
dataFineQuadrimestre = datetime.strptime("31-01-2021", "%d-%m-%y") #poi ovviamente va modificato il 2021
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
                s = res.text
                dataVotoHtml = driver.find_element_by_xpath('//*[@id="sheet-sezioneDidargo:panel-votiGiornalieri:form"]/fieldset[1]/table/tbody/tr/td[2]/b')
                dataVoto = datetime.strptime(dataVotoHtml, "%d-%m-%y")
                s = re.sub("[a-zA-z\s()$&+,:;=?@#|'<>^*()%!-]", '', s) #rimuove tutti i caratteri dalla stringa a parte i numeri e i punti
                if(s != None and s != ""): 
                    s = float(s)
                    if(dataVoto <= dataFineQuadrimestre):
                        mediaPrimoQuad += s
                        mediaPrimoQuad += 1
                    else:
                        mediaSecondoQuad += s
                        nVotiSecondoQuad += 1

        mediaPrimoQuad /= nVotiPrimoQuad
        mediaSecondoQuad /= nVotiSecondoQuad
        mediaPrimoQuad = 0.0
        nVotiPrimoQuad = 0.0
        mediaSecondoQuad = 0.0
        nVotiSecondoQuad = 0.0
        print("primo quad" + mediaPrimoQuad)
        print("secondo quad" + mediaSecondoQuad)
finally:
    pass


time.sleep(20)
driver.quit()
