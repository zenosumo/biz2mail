import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import sys
import time

# Define default values
DEFAULT_EXCEL_FILE = "bizlist.xls"
DEFAULT_COLUMN_VAT = "Codice Fiscale"
DEFAULT_COLUMN_COMPANY = "Denominazione Azienda"
DEFAULT_SEPARATOR = "|"
CSV_FILE_NAME = "bizlist.csv"
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILE_NAME = f"{SCRIPT_NAME}.log"
DEBUG_MODE = False  # Set to True to skip actual searches

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} [{default_value}]: ")
    return user_input if user_input else default_value

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
    extracted_df.loc[:, 'website'] = ""
    extracted_df.loc[:, 'email'] = ""
    extracted_df.loc[:, 'error'] = ""

    try:
        extracted_df.to_csv(CSV_FILE_NAME, sep=DEFAULT_SEPARATOR, index=False)
        print(f"CSV file created: {CSV_FILE_NAME}")
        return True
    except Exception as e:
        print(f"Error saving the CSV file: {e}")
        return False

def get_website_from_duckduckgo(vat, company_name):
    log_details = []

    if DEBUG_MODE:
        return f"http://example.com/{vat}/{company_name.replace(' ', '_')}"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    query = f"{vat} {company_name}"
    url = f"https://duckduckgo.com/html/?q={query}"
    log_details.append(f"Performing search for query: {query}")
    response = requests.get(url, headers=headers)
    log_details.append(f"Received status code: {response.status_code} for query: {query}")

    if response.status_code != 200:
        log_details.append(f"Error: Search request failed with status code {response.status_code} for query: {query}")
        with open(LOG_FILE_NAME, 'a') as log_file:
            log_file.write('\n'.join(log_details) + '\n')
        return None

    time.sleep(2)  # Add a delay to give time for the page to populate
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='result__a', href=True)

    if not results:
        log_details.append(f"No results found for query: {query}")
        with open(LOG_FILE_NAME, 'a') as log_file:
            log_file.write('\n'.join(log_details) + '\n')
        return None

    log_details.append(f"Found {len(results)} results for query: {query}:")
    for result in results:
        log_details.append(result['href'])

    with open(LOG_FILE_NAME, 'a') as log_file:
        log_file.write('\n'.join(log_details) + '\n')

    return results[0]['href']

def step_2_populate_website():
    try:
        df = pd.read_csv(CSV_FILE_NAME, sep=DEFAULT_SEPARATOR)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Ensure the website and error columns are of type string
    df['website'] = df['website'].astype(str)
    df['error'] = df['error'].astype(str)

    # Populate the website column
    for index, row in df.iterrows():
        vat = row[DEFAULT_COLUMN_VAT]
        company_name = row[DEFAULT_COLUMN_COMPANY]
        print(f"Searching for company: {company_name}, VAT: {vat}")
        website = get_website_from_duckduckgo(vat, company_name)
        if website:
            df.loc[index, 'website'] = website
        else:
            df.loc[index, 'error'] = "Website not found"

    try:
        df.to_csv(CSV_FILE_NAME, sep=DEFAULT_SEPARATOR, index=False)
        print(f"CSV file updated: {CSV_FILE_NAME}")
    except Exception as e:
        print(f"Error saving the updated CSV file: {e}")

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
            df = pd.read_csv(CSV_FILE_NAME, sep=DEFAULT_SEPARATOR)
            if df['website'].isnull().all() or (df['website'] == '').all():
                input("No website data found. Press Enter to proceed to step 2.")
                step_2_populate_website()
            else:
                print("Website data already populated. No further steps required.")
        except Exception as e:
            print(f"Error reading the CSV file: {e}")

if __name__ == "__main__":
    main()
