import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re
import os
import send_email

# Set up Selenium 
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Configuration
DOMAIN = "https://www.magazineluiza.com.br"
URL = f"{DOMAIN}/busca/notebooks/?from=clickSuggestion&filters=entity---notebook"
OUTPUT_DIR = 'Output'
ATTEMPTS = 3

def check_connection(url, attempts=3):
    """Checks if the website is accessible, making up to 3 attempts."""
    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raises exception if there's an HTTP error
            print(f"Connection successful on attempt {attempt + 1}.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"Unknown error: {e}")
            time.sleep(3)

    print(f"The website '{url}' appears to be down.")
    return False

def get_product_data(driver, url):
    """Scrapes product data from a single page."""
    driver.get(url)
    time.sleep(2)  # Add a delay to allow the page to fully load 
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

def process_data(products):
    """Processes product data and categorizes into 'Best' and 'Worst'."""
    df = pd.DataFrame(products)
    best = df[df['QTD_AVAL'] >= 100]
    worst = df[df['QTD_AVAL'] < 100]
    return best, worst

def save_data_to_excel(best, worst, output_dir):
    """Saves data to an Excel file."""
    os.makedirs(output_dir, exist_ok=True)
    with pd.ExcelWriter(os.path.join(output_dir, 'Notebooks.xlsx'), engine='xlsxwriter') as writer:
        best.to_excel(writer, sheet_name='Melhores', index=False)
        worst.to_excel(writer, sheet_name='Piores', index=False)
    print("Excel file 'Notebooks.xlsx' created successfully in 'Output'.")

    

if check_connection(URL):
    products = []
    for page_number in range(1, 3):
        url = f"{URL}&page={page_number}"
        products.extend(get_product_data(driver, url))

    best, worst = process_data(products)
    save_data_to_excel(best, worst, OUTPUT_DIR)

    driver.quit()

    subject_email = "Relatório Notebooks"
    content_html = """
    <!DOCTYPE html>
    <html>
    <body>
        <p>Olá, aqui está o seu relatório dos notebooks extraídos da Magazine Luiza.</p>
        <p>Atenciosamente,</p>
        <p>Robô🤖.</p>
    </body>
    </html>
    """
    to_send = "rosaa.estefanii@gmail.com"
    excel_file = os.path.abspath(os.path.join(OUTPUT_DIR, 'Notebooks.xlsx'))

    send_email(subject_email, content_html, to_send, excel_file)

else:
    print("Website is down.")
    driver.quit()