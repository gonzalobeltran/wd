
import time, datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

def login(usuario, pwd):
    driver.get("https://oficinajudicialvirtual.pjud.cl/home/index.php")
    
    driver.find_element(By.CLASS_NAME, "dropbtn").click()
    driver.find_element(By.XPATH, "//div[@id='myDropdown']/a").click()
    driver.find_element(By.ID, "uname").send_keys(usuario)
    driver.find_element(By.ID, "pword").send_keys(pwd)
    driver.find_element(By.ID, "login-submit").click()
    time.sleep(4)

    driver.find_element(By.CLASS_NAME, "fa-university").click()
    time.sleep(1)

    driver.find_element(By.ID, "familiaTab").click()
    time.sleep(1)

    driver.find_elements(By.CLASS_NAME, "switch")[6].click()
    time.sleep(2)

    # Selecciona todos los tipos de causas
    estadoCausas = Select(driver.find_element(By.ID, 'estadoCausaMisCauFam'))
    for i in range(12):
        estadoCausas.select_by_index(str(i))

def logout():
    driver.find_element(By.XPATH, "//a[@onclick='salir();']").click()
    time.sleep(1)

def nom_tribunal(t):
    res = t
    if (t[0] == '1'):
        res = '1º JUZGADO DE FAMILIA SANTIAGO'
    if (t[0] == '2'):
        res = '2º JUZGADO DE FAMILIA SANTIAGO'
    if (t[0] == '3'):
        res = '3º JUZGADO DE FAMILIA SANTIAGO'
    if (t[0] == '4'):
        res = '4º JUZGADO DE FAMILIA SANTIAGO'
    if (t[0] == 'C'):
        res = 'CENTRO DE MEDIDAS CAUTELARES DE SANTIAGO'
    return(res)

def busca_causa(causa, tribunal_en_lista, fur_en_lista):
    partes = causa.split('-')
    # Ingresa la causa a buscar
    Select(driver.find_element(By.ID, 'tipoMisCauFam')).select_by_value(partes[0])
    driver.find_element(By.ID, 'rolMisCauFam').clear()
    driver.find_element(By.ID, 'rolMisCauFam').send_keys(partes[1])
    driver.find_element(By.ID, 'anhoMisCauFam').clear()
    driver.find_element(By.ID, 'anhoMisCauFam').send_keys(partes[2])
    driver.find_element(By.ID, 'btnConsultaMisCauFam').click()

    # Espera el resultado
    time.sleep(1)

    furPJUD = ''
    tramite = ''
    desc = ''

    rows = driver.find_elements(By.XPATH, "//table[@id='dtaTableDetalleMisCauFam']/tbody/tr")
    
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        if len(tds) == 7:
            tribunal_en_tabla = nom_tribunal(tds[2].text.strip())
            if tribunal_en_tabla == tribunal_en_lista:
                tds[0].find_element(By.TAG_NAME, 'a').click()
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'movimientoFam')))
                cols = driver.find_elements(By.XPATH, "//div[@id='movimientoFam']/div/div/table/tbody/tr/td")
                if len(cols) >= 7:
                    tramite = cols[4].text.strip()
                    desc = cols[5].text.strip()                    
                    fur = cols[6].text.strip()
                    fur = fur[:6] + fur[8:]
                    furPJUD = fur.replace('/','-')
                driver.find_element(By.CLASS_NAME, 'close').click()                  
    
    rit.append(causa)
    tribunal.append(tribunal_en_lista)
    ultima.append(fur_en_lista.strftime('%d-%m-%y'))
    ultimaPJUD.append(furPJUD)
    if ultima[-1] != furPJUD:
        revisar.append('Revisar ' + causa + ': ' + tramite + ', ' + desc)
    else:
        revisar.append('-')

def revisa_abogado(usuario, pwd, lista):
    login(usuario, pwd)
    for n in lista.index:
        busca_causa(lista['ROL/RIT'][n], lista['TRIBUNAL'][n], lista['FUR'][n])
    logout()
    guarda_excel()

def revisa_usuarios(lista):
    for n in lista.index:
        login(lista['RUT_PATROCINADO'][n], lista['CLAVE'][n])
        busca_causa(lista['ROL/RIT'][n], lista['TRIBUNAL'][n], lista['FUR'][n])
        logout()
    guarda_excel()

def guarda_excel():
    dict =  {'Rit': rit, 'Tribunal': tribunal, 'FUR': ultima, 'FUR PJUD': ultimaPJUD, 'Revisar': revisar}
    df = pd.DataFrame.from_dict(dict)
    df.to_excel('revisar.xlsx')

df = pd.read_excel('Carolina causas asignadas.xls','Asignadas')
activas = df[df['T/V'].isin(['D', 'T/R', 'V'])]

caro = activas[activas.ACCESO == 'CC']
franco = activas[activas.ACCESO == 'FG']
usuarios = activas[activas.ACCESO == 'U']

rit = []
tribunal = []
ultima = []
ultimaPJUD = []
revisar = []

driver = webdriver.Chrome()
driver.maximize_window()

revisa_usuarios(usuarios)
revisa_abogado('138245721', 'POllito-1010', caro)
revisa_abogado('128622497', 'Catalinabarra2614.', franco)

driver.close()


