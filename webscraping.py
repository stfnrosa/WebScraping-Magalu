import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

url = "https://www.magazineluiza.com.br/busca/notebook/?from=clickSuggestion"

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

driver.get(url)

# Espera até que os elementos estejam presentes
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-dxlmjS"))
    )
    page_content = driver.page_source
finally:
    driver.quit()

soup = BeautifulSoup(page_content, 'html.parser')

products = []

items = soup.find_all('li', class_="sc-fTyFcS iTkWie")
for item in items:
    product_title = item.find('h2', class_='sc-elxqWl kWTxnF')
    product_link = item.find('a', class_='sc-eBMEME uPWog sc-evdWiO gqyJd sc-evdWiO gqyJd')
    product_reviews = item.find('span', class_='sc-epqpcT jdMYP')
    
    if product_title and product_link:
        products.append({
            'title': product_title.text,
            'link': product_link['href'],
            'reviews': product_reviews.text if product_reviews else 'No reviews'
        })

df = pd.DataFrame(products)
print(df)

        