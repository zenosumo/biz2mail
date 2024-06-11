import pandas as pd
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


options = Options()
options.add_argument("--headless")
service = Service('/home/kris/bin/chromedriver')  # Use this if not in your PATH
driver = webdriver.Chrome(service=service, options=options)

# Define default values
DEFAULT_EXCEL_FILE = "bizlist.xls"
DEFAULT_COLUMN_VAT = "Codice Fiscale"
DEFAULT_COLUMN_COMPANY = "Denominazione Azienda"
DEFAULT_FIELD_SEPARATOR = "|"
DEFAULT_URL_SEPARATOR = "^"
CSV_FILE_NAME = "bizlist.csv"
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILE_NAME = f"{SCRIPT_NAME}.log"
DEBUG_MODE = False  # Set to True to skip actual searches

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} [{default_value}]: ")
    return user_input if user_input else default_value

def duckduckgo_search(search_term):
    try:
        results = DDGS().text(search_term, max_results=1)
        # Extract URLs from the results
        urls = [result['href'] for result in results if 'href' in result]
        return urls
    except Exception as err:
        print(f"An error occurred: {err}")
        return []

def step_1_generate_csv(excel_file, column_vat, column_company):
    try:
        df = pd.read_excel(excel_file, engine='xlrd')
    except ImportError as e:
        print("Error: Missing a required library. Please install the following library:")
        print("pip install xlrd")
        return False
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return False

    if column_vat not in df.columns:
        print(f"Error: Column '{column_vat}' not found in the Excel file.")
        return False
    if column_company not in df.columns:
        print(f"Error: Column '{column_company}' not found in the Excel file.")
        return False

    extracted_df = df[[column_vat, column_company]].copy()
    extracted_df['website'] = ""
    extracted_df['email'] = ""
    extracted_df['error'] = ""

    # Ensure the 'website' column is explicitly set to string type
    extracted_df = extracted_df.astype({"website": str})

    try:
        extracted_df.to_csv(CSV_FILE_NAME, sep=DEFAULT_FIELD_SEPARATOR, index=False)
        print(f"CSV file created: {CSV_FILE_NAME}")
        return True
    except Exception as e:
        print(f"Error saving the CSV file: {e}")
        return False

def step_2_populate_website():
    try:
        df = pd.read_csv(CSV_FILE_NAME, sep=DEFAULT_FIELD_SEPARATOR)

        # Ensure the 'website' column is explicitly set to string type
        df['website'] = df['website'].astype(str)

        for index, row in df.iterrows():
            company_name = row[DEFAULT_COLUMN_COMPANY]
            vat_code = row[DEFAULT_COLUMN_VAT]
            search_term = f"{company_name} {vat_code}"
            print(f"Searching for: {search_term}")
            urls = duckduckgo_search(search_term)
            df.at[index, 'website'] = DEFAULT_URL_SEPARATOR.join(urls)
            time.sleep(1)  # Be polite and avoid being blocked

        df.to_csv(CSV_FILE_NAME, sep=DEFAULT_FIELD_SEPARATOR, index=False)
        print(f"CSV file updated with websites: {CSV_FILE_NAME}")
    except Exception as e:
        print(f"An error occurred during website population: {e}")

def main():
    # Initialize log file
    with open(LOG_FILE_NAME, 'w') as log_file:
        log_file.write("Debug Log\n")

    # Determine the step to execute
    if not os.path.isfile(CSV_FILE_NAME):
        print("Step 1: Generating CSV file from Excel.")
        excel_file = get_user_input("Enter the path to the Excel file", DEFAULT_EXCEL_FILE)
        column_vat = get_user_input("Enter the name of the VAT column", DEFAULT_COLUMN_VAT)
        column_company = get_user_input("Enter the name of the Company column", DEFAULT_COLUMN_COMPANY)

        if step_1_generate_csv(excel_file, column_vat, column_company):
            input("Step 1 complete. Press Enter to proceed to step 2.")
            step_2_populate_website()
    else:
        print("CSV file already exists.")
        try:
            df = pd.read_csv(CSV_FILE_NAME, sep=DEFAULT_FIELD_SEPARATOR)
            if df['website'].isnull().all() or (df['website'] == '').all():
                input("No website data found. Press Enter to proceed to step 2.")
                step_2_populate_website()
            else:
                print("Website data already populated. No further steps required.")
        except Exception as e:
            print(f"Error reading the CSV file: {e}")

if __name__ == "__main__":
    main()
