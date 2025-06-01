import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Rutas indicadas
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

options = Options()
options.binary_location = brave_path

service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)

try:
    # Abrir login
    driver.get("http://localhost:5000/login")

    # Ingresar usuario y contraseña
    wait.until(EC.presence_of_element_located((By.ID, "correo"))).send_keys("bianca@gmail.com")
    driver.find_element(By.ID, "contraseña").send_keys("bianca123")
    driver.find_element(By.CSS_SELECTOR, "form#formLogin button[type='submit']").click()

    # Esperar cartelera (bienvenida)
    wait.until(EC.title_contains("Cartelera de Películas"))

    # Añadir la primera película para renta
    primera_pelicula_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rentar-btn")))
    primera_pelicula_btn.click()

    time.sleep(2)  # espera mensaje confirmación

    # Click en "Rentar ahora"
    boton_rentar_global = driver.find_element(By.ID, "rentar-global-btn")
    boton_rentar_global.click()

    # Esperar a que cargue la factura
    wait.until(EC.title_contains("Factura"))

    # Confirmar película en la factura
    filas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    if filas:
        print("✅ Película rentada aparece en la factura.")
    else:
        print("❌ No hay películas en la factura.")
        driver.quit()
        exit()
    time.sleep(5)
    # Eliminar película con botón
    boton_eliminar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-eliminar")))
    boton_eliminar.click()

    time.sleep(2)  # espera que se procese la eliminación y se recargue

    # Confirmar que no haya películas después de eliminar
    filas_post_eliminar = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    if not filas_post_eliminar:
        print("✅ Película eliminada correctamente de la factura.")
    else:
        print("❌ La película no se eliminó correctamente.")

finally:
    time.sleep(5)
    driver.quit()
