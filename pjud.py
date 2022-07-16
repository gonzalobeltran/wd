
import time, datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

def login(usuario, pwd):
    driver.get("https://oficinajudicialvirtual.pjud.cl/indexN.php#")

    driver.find_element(By.CLASS_NAME, "dropbtn").click()
    driver.find_element(By.ID, "btnSegClave").click()
    time.sleep(1)

    driver.find_element(By.ID, "rut").send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(pwd)
    driver.find_element(By.ID, "btnSegundaClaveIngresar").click()
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, "fa-university").click()
    time.sleep(1)

    driver.find_element(By.ID, "familiaTab").click()
    time.sleep(1)

    driver.find_elements(By.CLASS_NAME, "switch")[6].click()
    time.sleep(1)

    # Selecciona todos los tipos de causas
    estadoCausas = Select(driver.find_element(By.ID, 'estadoCausaMisCauFam'))
    for i in range(12):
        estadoCausas.select_by_index(str(i))

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

def busca_causa(causa):
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

    # Extrae Rit y Tribunal de la tabla
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    col = soup.find('table', id='dtaTableDetalleMisCauFam').find('tbody').find('tr').find_all('td')
    if len(col) == 7:
        rit = col[1].get_text().strip()
        tribunal = nom_tribunal(col[2].get_text().strip())
    else:
        rit = 'No encontrado'
        tribunal = 'No encontrado'

    # Abre el modal con información sobre la causa
    driver.find_element(By.XPATH, "//table[@id='dtaTableDetalleMisCauFam']/tbody/tr/td/a").click()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'movimientoFam')))
 
    # Extrae fecha de última resolución
    soupModal = BeautifulSoup(driver.page_source, 'html.parser')
    filaModal = soupModal.find('div', id='movimientoFam').find('table').find('tbody').find('tr')
    if filaModal == None:
        ultima = ''
    else:
        celdas = filaModal.find_all('td')
        fur = celdas[6].get_text().strip()
        fur = fur[:6] + fur[8:]
        ultima = fur.replace('/','-')
    driver.find_element(By.CLASS_NAME, 'close').click()
    return (rit, tribunal, ultima)


df = pd.read_excel('causas.xls','Asignadas')
activas = df[df['T/V'].isin(['D', 'T/R', 'V'])]

caro = activas[activas.ACCESO == 'CC']
franco = activas[activas.ACCESO == 'FG']

rit = []
tribunal = []
tribunalPJUD = []
ultima = []
ultimaPJUD = []
revisar = []

driver = webdriver.Chrome()
driver.maximize_window()
login('13824572', 'Encanto1981')

for n in caro.index:
    r, t, u = busca_causa(caro['ROL/RIT'][n])
    rit.append(r)
    tribunal.append(caro['TRIBUNAL'][n])
    tribunalPJUD.append(t)
    ultima.append(caro['última resolución'][n].strftime('%d-%m-%y'))
    ultimaPJUD.append(u)
    if (tribunal[-1] != t) or (ultima[-1] != u):
        revisar.append('Revisar ' + r)
    else:
        revisar.append('')


dict =  {'Rit': rit, 'Tribunal': tribunal, 'Tribunal PJUD': tribunalPJUD, 'FUR': ultima, 'FUR PJUD': ultimaPJUD, 'Revisar': revisar}
df = pd.DataFrame.from_dict(dict)

df.to_excel('resultado.xlsx')
driver.close()
