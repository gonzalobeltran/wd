
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://sso.uc.cl")
driver.find_element(By.ID, "username").send_keys("gbeltran")
driver.find_element(By.ID, "password").send_keys("1787ZSIomYyi")
driver.find_element(By.CLASS_NAME, "btn-submit").click()
time.sleep(1)

driver.get("https://sso.uc.cl/cas/login?service=https://rrhh.uc.cl/psp/hcm91prd/?cmd=start%26languageCd=ESP")
driver.find_element(By.ID, "CUS_AUTOSERVICIO_EMPLEADO$0").click()
time.sleep(2)

driver.find_element(By.ID, "CUS_REMUNERACIONES$1").click()

dates = list(map(lambda x: x.text, driver.find_elements(By.XPATH, "//a[contains(@id,'VIEW')]")[2:]))
fechas = []
for f in dates:
    partes = f.split('/')
    fechas.append(partes[1] + '-' + partes[0] + '-' + partes[2])

montos = list(map(lambda x: x.text, driver.find_elements(By.XPATH, "//span[contains(@id,'CUS_LIQSUEL_WRK_CUS_LCL_PAGO_NETO')]")))

for i in range(0, len(fechas)):
    print(fechas[i] + ': ' + montos[i])

driver.close()
