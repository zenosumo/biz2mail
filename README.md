
# Excel to CSV Extractor with Web Data Enhancement

### Purpose
The "Excel to CSV Extractor with Web Data Enhancement" is an enhanced Python-based tool designed not only to extract specific columns from an Excel file into a CSV file but also to enrich the CSV with web-scraped data such as websites and emails of the companies listed. This tool is ideal for users requiring comprehensive data assembly from various sources into a manageable format.

### How It Works
The tool operates in three main steps:
1. **CSV Generation**: Takes an Excel file as input, extracts specified columns (default: "Codice Fiscale" and "Denominazione Azienda"), and generates a CSV file. These columns has to be unique.
2. **Website Data Enrichment**: Uses DuckDuckGo search to retrieve the first three URLs related to the company and appends these URLs to the CSV.
3. **Email Data Enrichment**: Extracts emails from the URLs and appends this data to the CSV.

The script ensures robust error handling for missing files, columns, and web scraping anomalies.

## Installation

### Prerequisites
- Python installed on your system.
- Required libraries: `pandas`, `openpyxl`, `xlrd`, `requests`, `duckduckgo_search`.

### Setup Instructions

1. **Install Python**: Download from the [official Python website](https://www.python.org/downloads/).

2. **Set Up Virtual Environment**:
   ```shell
   python -m venv bizenv
   source bizenv/bin/activate  # Unix/MacOS
   bizenv\Scripts\activate  # Windows
   ```

3. **Install Required Packages**:
   ```shell
   pip install pandas xlrd requests duckduckgo_search
   ```

4. **Deactivate the Virtual Environment**:
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

The detailed error logging in the script will assist in troubleshooting issues related to file reading and web scraping.
