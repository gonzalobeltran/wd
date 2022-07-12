
import time, re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://sso.uc.cl")
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys("gbeltran")

elem = driver.find_element(By.ID, "password")
elem.clear()
elem.send_keys("1787ZSIomYyi")

elem.send_keys(Keys.RETURN)
time.sleep(1)

driver.get("https://sso.uc.cl/cas/login?service=https://rrhh.uc.cl/psp/hcm91prd/?cmd=start%26languageCd=ESP")
elem = driver.find_element(By.ID, "CUS_AUTOSERVICIO_EMPLEADO$0")
elem.click()
time.sleep(1)

elem = driver.find_element(By.ID, "CUS_REMUNERACIONES$1")
elem.click()

pagina = driver.page_source

soup = BeautifulSoup(pagina, 'html.parser')

fechas = []
for fecha in soup.findAll('a', id=re.compile('VIEW.*')):
    if (fecha.get_text() != 'Fecha Pago'):
        fechas.append(fecha.get_text())

neto = []
for pago in soup.findAll('span', id=re.compile('CUS_LIQSUEL_WRK_CUS_LCL_PAGO_NETO.*')):
    neto.append(pago.get_text())

dict = {'Fecha': fechas, 'Sueldo': neto}
df = pd.DataFrame.from_dict(dict)
df.to_excel('liquidaciones.xlsx')

driver.close()
