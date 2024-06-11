
# Excel to CSV Extractor with Web Data Enhancement

### Purpose
The "Excel to CSV Extractor with Web Data Enhancement" is an enhanced Python-based tool designed not only to extract specific columns from an Excel file into a CSV file but also to enrich the CSV with web-scraped data such as websites and emails of the companies listed. This tool is ideal for users requiring comprehensive data assembly from various sources into a manageable format.

### How It Works
The tool operates in two main steps:
1. **CSV Generation**: Takes an Excel file as input, extracts specified columns (default: "Codice Fiscale" and "Denominazione Azienda"), and generates a CSV file.
2. **Data Enrichment**: Uses web scraping to retrieve additional information like company websites and emails, appending this data to the CSV.

The script ensures robust error handling for missing files, columns, and web scraping anomalies.

## Installation

### Prerequisites
- Python installed on your system.
- ChromeDriver executable for Selenium-based web scraping. Download it [here](https://googlechromelabs.github.io/chrome-for-testing).

### Setup Instructions

1. **Install Python**: Download from the [official Python website](https://www.python.org/downloads/).

2. **Download ChromeDriver**: Ensure you have the ChromeDriver which matches your Chrome version. Download it from [Chrome Labs](https://googlechromelabs.github.io/chrome-for-testing).

3. **Set Up Virtual Environment**:
   ```shell
   python -m venv bizenv
   source bizenv/bin/activate  # Unix/MacOS
   bizenv\Scripts\activate  # Windows
   ```

4. **Install Required Packages**:
   ```shell
   pip install pandas openpyxl xlrd requests beautifulsoup4 selenium
   ```

5. **Deactivate the Virtual Environment**:
   ```shell
   deactivate
   ```

## Usage

### Inputs
- **Excel File**: Path to the Excel file.
- **Columns**: Names of the VAT and company columns (default settings provided).

### Running the Script
Navigate to the script directory and execute:
```shell
python biz2mail.py
```

Follow the prompts to input the Excel file path and column names. The script will first generate a CSV file and then proceed to enrich it with websites and emails fetched online.

### Example Usage
```shell
Enter the path to the Excel file [bizlist.xls]: 
Enter the name of the VAT column [Codice Fiscale]: 
Enter the name of the Company column [Denominazione Azienda]:
```

## Troubleshooting
- Ensure all dependencies are correctly installed.
- Verify that the ChromeDriver path is correctly set in the script.

The detailed error logging in the script will assist in troubleshooting issues related to file reading and web scraping.
