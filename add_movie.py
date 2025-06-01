from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configuración para Brave en Windows
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')

options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("--start-maximized")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. Iniciar sesión como admin
    driver.get("http://127.0.0.1:5000/login")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "correo")))
    driver.find_element(By.NAME, "correo").send_keys("admin@admin.com")
    driver.find_element(By.NAME, "contraseña").send_keys("admin" + Keys.ENTER)

    # 2. Esperar redirección a la vista admin
    WebDriverWait(driver, 5).until(EC.title_contains("Admin"))

    # 3. Abrir formulario de agregar película
    boton_agregar = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btn-agregar-pelicula")))
    boton_agregar.click()

    # 4. Rellenar formulario
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "formPelicula")))
    driver.find_element(By.ID, "titulo").send_keys("Oppenheimer")
    driver.find_element(By.ID, "año").send_keys("2024")
    driver.find_element(By.ID, "genero").send_keys("Suspenso")
    driver.find_element(By.ID, "director").send_keys("Christopher Nolan")
    driver.find_element(By.ID, "precio").send_keys("99")

    # Subir imagen (usa una imagen válida en la misma carpeta)
    imagen_path = os.path.abspath("poster_ejemplo.jpg")
    driver.find_element(By.ID, "poster").send_keys(imagen_path)

    # 5. Enviar formulario
    driver.find_element(By.CSS_SELECTOR, "#formPelicula button[type='submit']").click()

    # 6. Esperar mensaje de éxito o recarga de cartelera
    time.sleep(2)  # ajustable según cómo manejes la respuesta del formulario

    print("✅ Prueba completa: el admin ha agregado una película exitosamente.")

except Exception as e:
    print(f"❌ Error en prueba admin agrega película:\n{e}")

finally:
    time.sleep(3)
    driver.quit()
