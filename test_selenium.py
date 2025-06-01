from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import random

# Rutas en tu sistema Windows
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

# Configurar navegador Brave
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("--start-maximized")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Generar usuario de prueba
usuario_random = f"usuario{random.randint(1000,9999)}"
correo = f"{usuario_random}@gmail.com"
contraseña = "prueba123"

try:
    driver.get("http://127.0.0.1:5000")
    time.sleep(1)
    driver.find_element(By.NAME, "nombre").send_keys("Test Selenium")
    driver.find_element(By.NAME, "correo").send_keys(correo)
    driver.find_element(By.NAME, "usuario").send_keys(usuario_random)
    driver.find_element(By.NAME, "contraseña").send_keys(contraseña)
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)

    driver.get("http://127.0.0.1:5000/login")
    time.sleep(1)
    driver.find_element(By.NAME, "correo").send_keys(correo)
    driver.find_element(By.NAME, "contraseña").send_keys(contraseña + Keys.ENTER)
    time.sleep(2)

    assert "bienvenida" in driver.current_url

finally:
    driver.quit()
