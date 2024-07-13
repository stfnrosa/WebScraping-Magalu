import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import os

# Constantes
DOMAIN = "https://www.magaazineluiza.com.br"
URL = f"{DOMAIN}/busca/notebooks/?from=clickSuggestion&filters=entity---notebook"
OUTPUT_DIR = 'Output'
ATTEMPTS = 3

def verificar_conexao(url, attempts=3):
    """Verifica a conexão com o site, realizando até 3 tentativas."""
    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Lança exceção se houver erro HTTP
            print(f"Conexão estabelecida com sucesso na tentativa {attempt+1}.")
            return True  # Conexão bem-sucedida
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt+1} de conexão falhou: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            time.sleep(3)

    print(f"O site '{url}' parece estar fora do ar.")
    return False  # Todas as tentativas falharam

def obter_dados_dos_produtos(driver, url):
    """Coleta os dados dos produtos de uma página."""
    driver.get(url)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    items = soup.find_all('li', class_="sc-fTyFcS iTkWie")

    products = []
    for item in items:
        product_title = item.find('h2', class_='sc-elxqWl kWTxnF')
        product_link = item.find('a', class_='sc-eBMEME uPWog sc-evdWiO gqyJd sc-evdWiO gqyJd')
        product_reviews = item.find('span', class_='sc-epqpcT jdMYPv')

        if product_title and product_link:
            reviews_number = None
            if product_reviews:
                reviews_number = int(re.findall(r'\(([^)]+)\)', product_reviews.text)[0])

            if reviews_number:
                products.append({
                    'PRODUTO': product_title.text.strip(),
                    'QTD_AVAL': reviews_number,
                    'URL': DOMAIN + product_link['href']
                })
    return products

def processar_dados(products):
    """Processa os dados dos produtos e separa em "Melhores" e "Piores"."""
    df = pd.DataFrame(products)
    melhores = df[df['QTD_AVAL'] >= 100]
    piores = df[df['QTD_AVAL'] < 100]
    return melhores, piores

def salvar_dados_excel(melhores, piores, output_dir):
    """Salva os dados em um arquivo Excel."""
    os.makedirs(output_dir, exist_ok=True)
    with pd.ExcelWriter(os.path.join(output_dir, 'Notebooks.xlsx'), engine='xlsxwriter') as writer:
        melhores.to_excel(writer, sheet_name='Melhores', index=False)
        piores.to_excel(writer, sheet_name='Piores', index=False)
    print("Arquivo Excel 'Notebooks.xlsx' criado com sucesso em 'Output'.")

# Configuração do Selenium
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

if verificar_conexao(URL):
    products = []
    for page_number in range(1, 3):
        url = f"{URL}&page={page_number}"
        products.extend(obter_dados_dos_produtos(driver, url))

    melhores, piores = processar_dados(products)
    salvar_dados_excel(melhores, piores, OUTPUT_DIR)

    driver.quit()
else:
    print("O site está fora do ar. Encerrando a execução.")
    driver.quit()