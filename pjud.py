
import time, re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.get("https://oficinajudicialvirtual.pjud.cl/indexN.php#")

driver.find_element(By.CLASS_NAME, "dropbtn").click()
driver.find_element(By.ID, "btnSegClave").click()
time.sleep(1)

driver.find_element(By.ID, "rut").send_keys("13824572")
driver.find_element(By.ID, "password").send_keys("Encanto1981")
driver.find_element(By.ID, "btnSegundaClaveIngresar").click()
time.sleep(2)

driver.find_element(By.CLASS_NAME, "fa-university").click()
time.sleep(1)

driver.find_element(By.ID, "familiaTab").click()

# Tiempo para abrir filtro manualmente
time.sleep(10)

# Selecciona todos los tipos de causas
estadoCausas = Select(driver.find_element(By.ID, 'estadoCausaMisCauFam'))
for i in range(12):
    estadoCausas.select_by_index(str(i))

rit = []
ultima = []
lista = ['F-9183-2019', 'F-8255-2021']

for causa in lista:
    partes = causa.split('-')
    # Ingresa la causa a buscar
    Select(driver.find_element(By.ID, 'tipoMisCauFam')).select_by_value(partes[0])
    driver.find_element(By.ID, 'rolMisCauFam').clear()
    driver.find_element(By.ID, 'rolMisCauFam').send_keys(partes[1])
    driver.find_element(By.ID, 'anhoMisCauFam').clear()
    driver.find_element(By.ID, 'anhoMisCauFam').send_keys(partes[2])
    driver.find_element(By.ID, 'btnConsultaMisCauFam').click()

    # Espera el resultado
    time.sleep(2)

    # Extrae el No. de Rit de la tabla
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    col = soup.find('table', id='dtaTableDetalleMisCauFam').find('tbody').find('tr').find_all('td')
    if len(col) == 7:
        rit.append(col[1].get_text().strip()) 
    else:
        rit.append('No encontrado')

    # Abre el modal con información sobre la causa
    driver.find_element(By.XPATH, "//table[@id='dtaTableDetalleMisCauFam']/tbody/tr/td/a").click()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'movimientoFam')))
 
    # Extrae fecha de última resolución
    soupModal = BeautifulSoup(driver.page_source, 'html.parser')
    filaModal = soupModal.find('div', id='movimientoFam').find('table').find('tbody').find('tr')
    if filaModal == None:
        ultima.append('')
    else:
        celdas = filaModal.find_all('td')
        ultima.append(celdas[6].get_text().strip())
    driver.find_element(By.CLASS_NAME, 'close').click()
  

dict =  {'Rit': rit, 'Fecha Ultima Resolución': ultima}
df = pd.DataFrame.from_dict(dict)

df.to_excel('causas.xlsx')
driver.close()
