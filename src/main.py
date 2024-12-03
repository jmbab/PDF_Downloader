# PDF DOWNLOADER & CHECKER & REGISTER FROM/TO URLs IN EXCEL FILES
# Jean M. Babonneau | Nov. 2024 | MIT License

# MODULAR PART 1: MAIN ORCHESTRATION
# This script follows the principle of "separation of concerns" by delegating specific tasks 
# (like downloading PDFs or updating metadata) to specialized modules.
# This script serves as the entry point for the complete PDF downloader program 
# for orchestrating the entire workflow in a modular and maintainable manner.
# It performs the following tasks:
# 1. Loads the Excel file containing the source data (URLs, BRnum, etc.).
# 2. Initiates threaded execution for URL validation and PDF downloading.
# 3. Updates the metadata file to reflect the download status of each BRnum.
# 4. Validates the consistency between the source data and the metadata file.
# It orchestrates the overall workflow by importing and using functions from other modular scripts.

# main.py

from load_excel import load_excel
from validate_urls import get_valid_url
from download_pdf import download_pdf
from update_metadata import update_metadata
from threaded_executor import run_threaded_execution
import pandas as pd

# Define paths and column names for the files and data we'll process
excel_file_path = '../data/GRI_2017_2020.xlsx'
metadata_file_path = '../metadata/Metadata2024.xlsx'
download_folder = '../downloads'
primary_col = 'Pdf_URL'
alternative_col = 'Report Html Address'
brnum_col = 'BRnum'

# Function to validate metadata consistency
def validate_metadata(source_file_path, metadata_file_path, brnum_col):
    try:
        # Load source data and metadata
        source_df = pd.read_excel(source_file_path)
        metadata_df = pd.read_excel(metadata_file_path)

        # Extract BRnum lists
        source_brnums = set(source_df[brnum_col].dropna().unique())
        metadata_brnums = set(metadata_df["BRnum"].dropna().unique())

        # Check for missing BRnum entries
        missing_brnums = source_brnums - metadata_brnums
        if missing_brnums:
            print(f"Warning: The following BRnum entries are missing in the metadata file: {missing_brnums}")
        else:
            print("Validation successful: All BRnum entries are accounted for in the metadata file.")
    except Exception as e:
        print(f"Error during metadata validation: {e}")

def main():
    # Step 1: Load Excel data
    print("Loading Excel data...")
    df = load_excel(excel_file_path)
    if df is None:
        exit("Failed to load the Excel file.")
    print("Excel data loaded successfully.")
    
    # Step 2: Start threaded execution for URL validation and PDF downloading
    print("Starting threaded execution for URL validation and downloading...")
    results = run_threaded_execution(df, download_folder, metadata_file_path, primary_col, alternative_col, brnum_col)
    print(f"Threaded execution completed with results: {results}")

    # Step 3: Validate that all BRnum entries are accounted for in the metadata file
    print("Validating metadata file...")
    validate_metadata(excel_file_path, metadata_file_path, brnum_col)
    print("Validation completed.")

# Entry point for the script
if __name__ == "__main__":
    print("Starting the main process.")
    main()
    print("Process completed.")
