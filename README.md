
# Excel to CSV Extractor

## Description

### Purpose
The "Excel to CSV Extractor" is a Python-based tool designed to extract specific columns from an Excel file and save the data into a CSV file. This tool is particularly useful for users who need to transform large datasets from Excel format to a more versatile CSV format with custom separators.

### How It Works
The tool takes an Excel file as input, extracts two specified columns (by default, "Codice Fiscale" and "Denominazione Azienda"), and generates a CSV file with these columns. The resulting CSV file uses a custom separator (default is `|`). The script includes error handling for missing files and columns, ensuring a robust and user-friendly experience.

## Installation

### Step 1: Install Python

First, you need to have Python installed on your system. You can download the latest version of Python from the [official Python website](https://www.python.org/downloads/).

### Step 2: Install Python Environment Extension

To create and manage Python virtual environments, you can use `venv`, which is included in Python 3.3 and later.

### Step 3: Create and Activate a Virtual Environment

Open your terminal or command prompt and execute the following commands:

\`\`\`bash
# Navigate to your project directory
cd /path/to/your/project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
\`\`\`

### Step 4: Install Required Packages

With the virtual environment activated, install the required packages using `pip`:

\`\`\`bash
pip install pandas openpyxl xlrd
\`\`\`

### Step 5: Deactivate the Virtual Environment

Once you are done using the virtual environment, you can deactivate it by running:

\`\`\`bash
deactivate
\`\`\`

## Usage

### Inputs
- **Excel File**: The path to the Excel file you want to process.
- **VAT Column**: The name of the column containing VAT numbers (default: "Codice Fiscale").
- **Company Column**: The name of the column containing company names (default: "Denominazione Azienda").

### How to Run the Script

1. **Run the Script:**

   With the virtual environment activated, you can run the script by navigating to the directory containing your script and executing:

   \`\`\`bash
   python biz2mail.py
   \`\`\`

2. **Provide Inputs:**

   When prompted, provide the path to the Excel file and the column names. If you press Enter without typing anything, the script will use the default values.

### Example Usage

\`\`\`bash
Enter the path to the Excel file [bizlist.xls]: 
Enter the name of the VAT column [Codice Fiscale]: 
Enter the name of the Company column [Denominazione Azienda]:
\`\`\`

If the file and columns are valid, the script will create a CSV file in the same directory as the Excel file, with the same name but a `.csv` extension.
