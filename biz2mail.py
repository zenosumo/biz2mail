import pandas as pd
import os
import sys
import time
import re
import requests
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# Define default values
DEFAULT_COLUMN_VAT = "Codice Fiscale"
DEFAULT_COLUMN_COMPANY = "Denominazione Azienda"
DEFAULT_FIELD_SEPARATOR = "|"
DEFAULT_URL_SEPARATOR = ";"
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
LOG_FILE_NAME = f"{SCRIPT_NAME}.log"
DEBUG_MODE = False  # Set to True to skip actual searches

def get_user_input(prompt, default_value):
    """Get user input with a default value."""
    user_input = input(f"{prompt} [{default_value}]: ")
    return user_input if user_input else default_value

def list_files(extension):
    """List all files in the current directory with the given extension, excluding resolved files."""
    return [f for f in os.listdir() if f.endswith(extension) and "-resolved" not in f]

def duckduckgo_search(search_term):
    """Search for a term using DuckDuckGo and return the first URL."""
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
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            page_content = response.text
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_content)
            return list(set(emails))  # Return unique emails
        else:
            print(f"Failed to retrieve the page: {url}")
            return []
    except requests.Timeout:
        print(f"Timeout occurred while fetching the URL {url}")
        return "timeout"
    except (requests.RequestException, requests.Timeout) as e:
        print(f"An error occurred while fetching the URL {url}: {e}")
        return []

def get_root_url(url):
    """Get the root URL from a given URL."""
    parsed_url = urlparse(url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    return root_url

def step_1_generate_csv():
    """Generate a CSV file from the given Excel file."""
    excel_files = list_files('.xls') + list_files('.xlsx')
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
    csv_file_name = f"{os.path.splitext(excel_file)[0]}.csv"
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
        extracted_df.to_csv(csv_file_name, sep=DEFAULT_FIELD_SEPARATOR, index=False)
        print(f"CSV file created: {csv_file_name}")
    except Exception as e:
        print(f"Error saving the CSV file: {e}")
        return False

    return True

def populate_website_email():
    """Populate the website and email columns in the CSV file."""
    csv_files = list_files('.csv')
    if not csv_files:
        print("No CSV files found in the current directory.")
        return False

    print("Select a CSV file to use:")
    for idx, file in enumerate(csv_files, 1):
        print(f"{idx}: {file}")
    print("Q: Exit")

    file_choice = input("Enter the number of the file to use or Q to exit: ").strip()
    if file_choice.lower() == 'q':
        print("Exiting.")
        return
    if not file_choice.isdigit() or int(file_choice) < 1 or int(file_choice) > len(csv_files):
        print("Invalid choice.")
        return False

    csv_file = csv_files[int(file_choice) - 1]
    resolved_file = f"{os.path.splitext(csv_file)[0]}-resolved.csv"
    
    try:
        df = pd.read_csv(csv_file, sep=DEFAULT_FIELD_SEPARATOR, dtype=str).fillna('')
        
        if os.path.exists(resolved_file):
            df_resolved = pd.read_csv(resolved_file, sep=DEFAULT_FIELD_SEPARATOR, dtype=str).fillna('')
        else:
            df_resolved = pd.DataFrame(columns=df.columns)  # Create an empty DataFrame for resolved records

        total_records = len(df)
        for index, row in df.iterrows():
            if row['error'].strip():  # Skip records with existing errors
                continue
            if not row['website'].strip() or not row['email'].strip():  # Process only if website or email is not populated
                if not row['website'].strip():  # Search for website if not populated
                    company_name = row[DEFAULT_COLUMN_COMPANY]
                    vat_code = row[DEFAULT_COLUMN_VAT]
                    search_term = f"{company_name} {vat_code} -\"www.ufficiocamerale.it\""
                    print(f"Searching {index + 1}/{total_records}: {company_name}")
                    urls = duckduckgo_search(search_term)
                    if urls:
                        df.at[index, 'website'] = DEFAULT_URL_SEPARATOR.join(urls)
                    else:
                        df.at[index, 'error'] = "No website found"
                        continue  # Skip to next record if no website found

                # If website is populated, search for email
                urls = df.at[index, 'website'].split(DEFAULT_URL_SEPARATOR)
                all_emails = set()  # Use a set to avoid duplicates
                errors = []

                for url in urls:
                    emails = extract_emails(url)
                    if emails == "timeout":
                        df.at[index, 'error'] = "timeout"
                        break
                    if emails:
                        all_emails.update(emails)
                        break  # Stop after finding emails at the first URL
                    else:
                        root_url = get_root_url(url)
                        root_emails = extract_emails(root_url)
                        if root_emails == "timeout":
                            df.at[index, 'error'] = "timeout"
                            break
                        if root_emails:
                            all_emails.update(root_emails)
                            break
                        else:
                            errors.append(f"No emails found")

                df.at[index, 'email'] = DEFAULT_URL_SEPARATOR.join(all_emails) if all_emails else ''
                if not all_emails:
                    df.at[index, 'error'] = DEFAULT_URL_SEPARATOR.join(errors) if errors else "No emails found"
                else:
                    df.at[index, 'error'] = "no"

                # Save the record to the resolve file if both website and email are found
                if df.at[index, 'website'].strip() and df.at[index, 'email'].strip():
                    df_resolved = pd.concat([df_resolved, df.iloc[[index]]]).drop_duplicates()

                # Save to CSV after each update
                df.to_csv(csv_file, sep=DEFAULT_FIELD_SEPARATOR, index=False)
                df_resolved.to_csv(resolved_file, sep=DEFAULT_FIELD_SEPARATOR, index=False)
                print(f"Updated record {index + 1}/{total_records}")
                time.sleep(1)  # Be polite and avoid being blocked

        print(f"CSV files updated: {csv_file} and {resolved_file}")
    except Exception as e:
        print(f"An error occurred during website and email population: {e}")

def main():
    """Main function to control the workflow."""
    # with open(LOG_FILE_NAME, 'w') as log_file:
    #     log_file.write("Debug Log\n")

    print("Choose a step to run:")
    print("1: Generate CSV from Excel")
    print("2: Populate website and email data in CSV")
    print("Q: Exit")
    choice = input("Enter your choice (1/2/Q): ").strip()
    
    if choice == '1':
        step_1_generate_csv()
    elif choice == '2':
        populate_website_email()
    elif choice.lower() == 'q':
        print("Exiting the script.")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
