from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import re
from datetime import datetime
from selenium.webdriver.chrome.options import Options

PATH = ".\chromedriver8" # "E:\GoogleDriver\chromedriver.exe"
options = Options()
options.headless = True
driver = webdriver.Chrome(PATH, chrome_options=options)

if not data.isEmpty(): 
    while True:
        c = input("Vuoi caricare i dati? [y o n]\n>")
        if c == "y":
            codicescuola = data.getCodice()
            username = data.getUsername()
            password = data.getPassword()
            break
        if c == "n":
            import dataInputUI
            codicescuola = dataInputUI.codScuola # sg18309
            username = dataInputUI.user
            password = dataInputUI.passw
            break
else:
    import dataInputUI
    codicescuola = dataInputUI.codScuola # sg18309
    username = dataInputUI.user
    password = dataInputUI.passw

# prima pagina
driver.get("http://"+codicescuola+".scuolanext.info")


login = False
while not login:
    try:
        inputUsername = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        inputPassword = driver.find_element_by_id("password")
        inputUsername.send_keys(username)
        inputPassword.send_keys(password)
        inputPassword.send_keys(Keys.RETURN)
    finally:
        login = True

if data.isEmpty():
    while True:
        c = input("Vuoi salvare i dati? [y o n]\n>")
        if c == "y":
            data.save(codicescuola, username, password)
            break
        if c == "n":
            break

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
#dataFineQuadrimestre = datetime.strptime("31-01-2021", "%d-%m-%y") #poi ovviamente va modificato il 2021
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
                #dataVoto = datetime.strptime(dataVotoHtml, "%d-%m-%y")
                s = re.sub("[a-zA-z\s()$&+,:;=?@#|'<>^*()%!-]", '', s) #rimuove tutti i caratteri dalla stringa a parte i numeri e i punti
                if(s != None and s != ""): 
                    s = float(s)
                    if(True): # dataVoto <= dataFineQuadrimestre
                        mediaPrimoQuad += s
                        nVotiPrimoQuad += 1
                    else:
                        mediaSecondoQuad += s
                        nVotiSecondoQuad += 1

        mediaPrimoQuad /= nVotiPrimoQuad
        #mediaSecondoQuad /= nVotiSecondoQuad

        print("primo quadrimestre: " + str(mediaPrimoQuad))
        #print("secondo quadrimestre" + mediaSecondoQuad)
        mediaPrimoQuad = 0.0
        nVotiPrimoQuad = 0.0
        mediaSecondoQuad = 0.0
        nVotiSecondoQuad = 0.0
finally:
    pass

driver.quit()
