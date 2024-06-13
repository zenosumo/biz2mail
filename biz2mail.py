import pandas as pd
import os
import sys
import time
import re
import requests
from duckduckgo_search import DDGS

# Define default values
DEFAULT_COLUMN_VAT = "Codice Fiscale"
DEFAULT_COLUMN_COMPANY = "Denominazione Azienda"
DEFAULT_FIELD_SEPARATOR = "|"
DEFAULT_URL_SEPARATOR = ";"
CSV_FILE_NAME = "bizlist.csv"
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILE_NAME = f"{SCRIPT_NAME}.log"
DEBUG_MODE = False  # Set to True to skip actual searches

def get_user_input(prompt, default_value):
    """Get user input with a default value."""
    user_input = input(f"{prompt} [{default_value}]: ")
    return user_input if user_input else default_value

def list_excel_files():
    """List all Excel files in the current directory."""
    excel_files = [f for f in os.listdir() if f.endswith('.xls') or f.endswith('.xlsx')]
    return excel_files

def duckduckgo_search(search_term):
    """Search for a term using DuckDuckGo and return the first 3 URLs."""
    try:
        results = DDGS().text(search_term, max_results=1)
        urls = [result['href'] for result in results if 'href' in result]
        return urls
    except Exception as err:
        print(f"An error occurred: {err}")
        return []

def extract_emails(url):
    """Extract emails from a given URL."""
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            page_content = response.text
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_content)
            return emails
        else:
            print(f"Failed to retrieve the page: {url}")
            return []
    except (requests.RequestException, requests.Timeout) as e:
        print(f"An error occurred while fetching the URL {url}: {e}")
        return []

def step_1_generate_csv():
    """Generate a CSV file from the given Excel file."""
    excel_files = list_excel_files()
    if not excel_files:
        print("No Excel files found in the current directory.")
        return False
    
    print("Select an Excel file to use:")
    for idx, file in enumerate(excel_files, 1):
        print(f"{idx}: {file}")
    print("Q: Exit")

    file_choice = input("Enter the number of the file to use or Q to exit: ").strip()
    if file_choice.lower() == 'q':
        print("Exiting.")
        return
    if not file_choice.isdigit() or int(file_choice) < 1 or int(file_choice) > len(excel_files):
        print("Invalid choice.")
        return False
    
    excel_file = excel_files[int(file_choice) - 1]
    column_vat = get_user_input("Enter the name of the VAT column", DEFAULT_COLUMN_VAT)
    column_company = get_user_input("Enter the name of the Company column", DEFAULT_COLUMN_COMPANY)

    try:
        df = pd.read_excel(excel_file, engine='openpyxl' if excel_file.endswith('xlsx') else 'xlrd')
    except ImportError as e:
        print("Error: Missing a required library. Please install the following library:")
        print("pip install xlrd openpyxl")
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

    # Ensure the 'website', 'email', and 'error' columns are explicitly set to string type
    extracted_df = extracted_df.astype({"website": str, "email": str, "error": str})

    try:
        extracted_df.to_csv(CSV_FILE_NAME, sep=DEFAULT_FIELD_SEPARATOR, index=False)
        print(f"CSV file created: {CSV_FILE_NAME}")
        return True
    except Exception as e:
        print(f"Error saving the CSV file: {e}")
        return False

def step_2_populate_website():
    """Populate the website column in the CSV file."""
    csv_file = get_user_input("Enter the path to the CSV file", CSV_FILE_NAME)
    try:
        df = pd.read_csv(csv_file, sep=DEFAULT_FIELD_SEPARATOR)
        
        # Ensure all columns are treated as strings
        df = df.astype(str).fillna('')
        
        total_records = len(df)
        for index, row in df.iterrows():
            company_name = row[DEFAULT_COLUMN_COMPANY]
            vat_code = row[DEFAULT_COLUMN_VAT]
            search_term = f"{company_name} {vat_code}"
            print(f"Searching {index + 1}/{total_records}: {search_term}")
            urls = duckduckgo_search(search_term)
            df.at[index, 'website'] = DEFAULT_URL_SEPARATOR.join(urls)

            # Save to CSV after each update
            df.to_csv(csv_file, sep=DEFAULT_FIELD_SEPARATOR, index=False)
            time.sleep(1)  # Be polite and avoid being blocked

        print(f"CSV file updated with websites: {csv_file}")
    except Exception as e:
        print(f"An error occurred during website population: {e}")

def step_3_populate_email():
    """Populate the email column in the CSV file."""
    csv_file = get_user_input("Enter the path to the CSV file", CSV_FILE_NAME)
    try:
        df = pd.read_csv(csv_file, sep=DEFAULT_FIELD_SEPARATOR)
        
        # Ensure all columns are treated as strings
        df = df.astype(str).fillna('')

        total_records = len(df)
        for index, row in df.iterrows():
            if row['website']:
                urls = row['website'].split(DEFAULT_URL_SEPARATOR)
                all_emails = []
                errors = []
                for url in urls:
                    emails = extract_emails(url)
                    if emails:
                        all_emails.extend(emails)
                    else:
                        errors.append(f"home page Timeout")

                df.at[index, 'email'] = DEFAULT_URL_SEPARATOR.join(all_emails) if all_emails else ''
                df.at[index, 'error'] = DEFAULT_URL_SEPARATOR.join(errors) if errors else ''

                # Save to CSV after each update
                df.to_csv(csv_file, sep=DEFAULT_FIELD_SEPARATOR, index=False)
                print(f"Updated email {index + 1}/{total_records}")
                time.sleep(0.2)  

        print(f"CSV file updated with emails: {csv_file}")
    except Exception as e:
        print(f"An error occurred during email population: {e}")

def main():
    """Main function to control the workflow."""
    with open(LOG_FILE_NAME, 'w') as log_file:
        log_file.write("Debug Log\n")

    print("Choose a step to run:")
    print("1: Generate CSV from Excel")
    print("2: Populate website data in CSV")
    print("3: Populate email data in CSV")
    print("Q: Exit")
    choice = input("Enter your choice (1/2/3/Q): ").strip()
    
    if choice == '1':
        step_1_generate_csv()
    elif choice == '2':
        step_2_populate_website()
    elif choice == '3':
        step_3_populate_email()
    elif choice.lower() == 'q':
        print("Exiting the script.")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
