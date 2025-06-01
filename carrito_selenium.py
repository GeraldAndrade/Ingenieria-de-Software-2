import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Rutas
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

options = Options()
options.binary_location = brave_path

service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)

try:
    # 1. Abrir login
    driver.get("http://localhost:5000/login")

    # 2. Ingresar correo y contraseña
    wait.until(EC.presence_of_element_located((By.ID, "correo"))).send_keys("bianca@gmail.com")
    driver.find_element(By.ID, "contraseña").send_keys("bianca123")
    driver.find_element(By.CSS_SELECTOR, "form#formLogin button[type='submit']").click()

    # 3. Esperar página cartelera (bienvenida)
    wait.until(EC.title_contains("Cartelera de Películas"))

    # 4. Agregar la primera película para renta
    primera_pelicula_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rentar-btn")))
    primera_pelicula_btn.click()

    # Esperar mensaje confirmación
    time.sleep(2)

    # 5. Clic en botón "Rentar ahora"
    boton_rentar_global = driver.find_element(By.ID, "rentar-global-btn")
    boton_rentar_global.click()

    # 6. Esperar a que cargue factura
    wait.until(EC.title_contains("Factura"))

    # 7. Verificar que haya películas rentadas
    filas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    if filas:
        print("✅ Película rentada aparece en la factura.")
    else:
        print("❌ No se encontró ninguna película en la factura.")

finally:
    time.sleep(5)
    driver.quit()
