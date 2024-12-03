# PDF DOWNLOADER & CHECKER & REGISTER FROM/TO URLs IN EXCEL FILES
# Jean M. Babonneau | Nov. 2024 | MIT License

# MODULAR PART 5: EXCEL LOADER
# This module adheres to the principle of "separation of concerns" by focusing solely on
# its own task. It is designed for maintainability and reuse.
# This module handles loading the source Excel file into a pandas DataFrame.
# It performs the following tasks:
# 1. Opens the specified Excel file.
# 2. Returns the content as a pandas DataFrame for further processing.
# 3. Handles errors such as missing or corrupt files.
# This ensures that the source data is correctly loaded and ready for processing.

# load_excel.py

import pandas as pd

# Function to load Excel file data
def load_excel(excel_file_path):
    # Opens the Excel file and returns a DataFrame.
    try:
        data = pd.read_excel(excel_file_path)
        print("Excel file opened successfully.")
        return data
    except FileNotFoundError:
        print("Error: The file was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        return None
