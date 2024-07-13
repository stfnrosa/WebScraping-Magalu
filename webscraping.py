import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import os

options = Options()
options.headless = True  # Opcional: executar em modo headless
driver = webdriver.Firefox(options=options)

domain = "https://www.magazineluiza.com.br"
base_url = "https://www.magazineluiza.com.br/busca/notebooks/?from=clickSuggestion&filters=entity---notebook"

products = []

for page_number in range(1, 3):  
    url = f"{base_url}&page={page_number}"
    driver.get(url)

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')

    items = soup.find_all('li', class_="sc-fTyFcS iTkWie")
    for item in items:
        product_title = item.find('h2', class_='sc-elxqWl kWTxnF')
        product_link = item.find('a', class_='sc-eBMEME uPWog sc-evdWiO gqyJd sc-evdWiO gqyJd')
        product_reviews = item.find('span', class_='sc-epqpcT jdMYPv')

        if product_title and product_link:
            reviews_number = None
            if product_reviews:
                reviews_number = int(re.findall(r'\(([^)]+)\)', product_reviews.text)[0]) 

            if reviews_number:  # Adiciona apenas produtos com avaliações
                products.append({
                    'PRODUTO': product_title.text,
                    'QTD_AVAL': reviews_number,
                    'URL': domain + product_link['href']
                })

df = pd.DataFrame(products)

# Criar a pasta Output se não existir
output_dir = 'Output'
os.makedirs(output_dir, exist_ok=True)

# Separar notebooks em "Melhores" e "Piores"
melhores = df[df['QTD_AVAL'] >= 100]
piores = df[df['QTD_AVAL'] < 100]

# Criar o arquivo Excel com múltiplas abas
with pd.ExcelWriter(os.path.join(output_dir, 'Notebooks.xlsx'), engine='xlsxwriter') as writer:
    melhores.to_excel(writer, sheet_name='Melhores', index=False)
    piores.to_excel(writer, sheet_name='Piores', index=False)

print("Arquivo Excel 'Notebooks.xlsx' criado com sucesso em 'Output'.")

        