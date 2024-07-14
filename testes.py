from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def scrape_produtos(webdriver):
    produtos = []
    pag_atual = 1

    while True:
        try:
            button_disabled = WebDriverWait(webdriver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@type="next" and @disabled]'))
            )
            break  
        except:
            button = WebDriverWait(webdriver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="next"]'))
            )
            button.click()
            WebDriverWait(webdriver, 10).until(
                EC.url_contains(f'page={pag_atual + 1}')
            )

            pag_atual += 1

            sleep(2) 

    return produtos

# Inicializa o navegador
driver = webdriver.Chrome()
driver.get("https://www.magazineluiza.com.br/busca/notbooks/?from=submit")

# Chama a função para coletar os produtos
produtos = scrape_produtos(driver)

# Fecha o navegador
driver.quit()

# Imprime a lista de produtos
print(produtos)