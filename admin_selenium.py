from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Rutas para Brave y Chromedriver
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("--start-maximized")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "correo").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "contraseña").send_keys("admin" + Keys.ENTER)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/admin"))

    # Busca un texto visible que indique que estás en admin
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Películas" in body_text or "Admin" in body_text or "Administración" in body_text

    print("✅ Login como admin exitoso y acceso a página admin confirmado.")

except Exception as e:
    print(f"❌ Error durante la prueba: {e}")

finally:
    driver.quit()
