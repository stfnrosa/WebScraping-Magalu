import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True  # Opcional: executar em modo headless
driver = webdriver.Firefox(options=options)

base_url = "https://www.magazineluiza.com.br/busca/notebook/?from=clickSuggestion"

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
            products.append({
                'title': product_title.text,
                'link': product_link['href'],
                'reviews': product_reviews.text if product_reviews else 'No reviews'
            })

driver.quit()

df = pd.DataFrame(products)
print(df)

        