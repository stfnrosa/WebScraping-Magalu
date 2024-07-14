import requests
import time
import re
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from send_email import send_email
from configs.configs_template_email import email_html_message, email_subject, recipient_email, excel_file_path
from configs.configs_spraping import DOMAIN, URL, OUTPUT_DIR, ATTEMPTS

# Selenium configuration
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)


def check_connection(url, attempts=3):
    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(f"Connection successful on attempt {attempt + 1}.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"Unknown error: {e}")
            time.sleep(3)
    print(f"The site '{url}' appears to be down.")
    return False

def fetch_product_data(driver):
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
                    'PRODUCT': product_title.text.strip(),
                    'REVIEWS_COUNT': reviews_number,
                    'URL': DOMAIN + product_link['href']
                })
    return products

def scrape_products(driver):
    products = []
    current_page = 1

    while True:
        print(f"Processing page {current_page}")
        products.extend(fetch_product_data(driver))

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@type="next" and @disabled]'))
            )
            break  
        except:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="next"]'))
            )
            next_button.click()
            WebDriverWait(driver, 10).until(
                EC.url_contains(f'page={current_page + 1}')
            )
            current_page += 1
            time.sleep(5) 

    return products

def process_data(products):
    df = pd.DataFrame(products)
    best_products = df[df['REVIEWS_COUNT'] >= 100]
    worst_products = df[df['REVIEWS_COUNT'] < 100]
    return best_products, worst_products

def save_to_excel(best_products, worst_products, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with pd.ExcelWriter(os.path.join(output_dir, 'Notebooks.xlsx'), engine='xlsxwriter') as writer:
        best_products.to_excel(writer, sheet_name='Best', index=False)
        worst_products.to_excel(writer, sheet_name='Worst', index=False)
    print("Excel file 'Notebooks.xlsx' successfully created in 'Output'.")

def main():
    if check_connection(URL):
        driver.get(URL)
        products = scrape_products(driver)

        best_products, worst_products = process_data(products)
        save_to_excel(best_products, worst_products, 'Output')

        driver.quit()

        

        send_email(recipient_email, email_subject, email_html_message, excel_file_path)
    else:
        print("The site is down. Ending execution.")
        driver.quit()

main()