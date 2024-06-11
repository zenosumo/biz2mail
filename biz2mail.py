import pandas as pd
import os
import csv

# Define default values
DEFAULT_EXCEL_FILE = "bizlist.xls"
DEFAULT_COLUMN_VAT = "Codice Fiscale"
DEFAULT_COLUMN_COMPANY = "Denominazione Azienda"
DEFAULT_SEPARATOR = "|"
CSV_FILE_NAME = "bizlist.csv"

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

def step_2_populate_website():
    try:
        df = pd.read_csv(CSV_FILE_NAME, sep=DEFAULT_SEPARATOR)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return

    # Placeholder for browsing and populating website
    for index, row in df.iterrows():
        df.loc[index, 'website'] = 'http://example.com'  # Replace with actual logic to fetch website

    try:
        df.to_csv(CSV_FILE_NAME, sep=DEFAULT_SEPARATOR, index=False)
        print(f"CSV file updated: {CSV_FILE_NAME}")
    except Exception as e:
        print(f"Error saving the updated CSV file: {e}")

def main():
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
