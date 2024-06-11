
import pandas as pd
import os

# Define default values
DEFAULT_EXCEL_FILE = "bizlist.xls"
DEFAULT_COLUMN_VAT = "Codice Fiscale"
DEFAULT_COLUMN_COMPANY = "Denominazione Azienda"
DEFAULT_SEPARATOR = "|"

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} [{default_value}]: ")
    return user_input if user_input else default_value

def main():
    # Get parameters from user input with defaults
    excel_file = get_user_input("Enter the path to the Excel file", DEFAULT_EXCEL_FILE)
    column_vat = get_user_input("Enter the name of the VAT column", DEFAULT_COLUMN_VAT)
    column_company = get_user_input("Enter the name of the Company column", DEFAULT_COLUMN_COMPANY)

    # Check if the Excel file exists
    if not os.path.isfile(excel_file):
        print(f"Error: The file '{excel_file}' does not exist.")
        return

    # Read the Excel file
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    # Check if the necessary columns exist
    if column_vat not in df.columns:
        print(f"Error: Column '{column_vat}' not found in the Excel file.")
        return
    if column_company not in df.columns:
        print(f"Error: Column '{column_company}' not found in the Excel file.")
        return

    # Extract the necessary columns
    extracted_df = df[[column_vat, column_company]]

    # Create the output CSV file name
    csv_file_name = os.path.splitext(excel_file)[0] + ".csv"

    # Save the DataFrame to a CSV file with the custom separator
    try:
        extracted_df.to_csv(csv_file_name, sep=DEFAULT_SEPARATOR, index=False)
        print(f"CSV file created: {csv_file_name}")
    except Exception as e:
        print(f"Error saving the CSV file: {e}")

if __name__ == "__main__":
    main()
