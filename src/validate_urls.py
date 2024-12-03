# PDF DOWNLOADER & CHECKER & REGISTER FROM/TO URLs IN EXCEL FILES
# Jean M. Babonneau | Nov. 2024 | MIT License

# MODULAR PART 6: URL VALIDATOR
# This module adheres to the principle of "separation of concerns" by focusing solely on
# its own task. It is designed for maintainability and reuse.
# This module is responsible for validating URLs before attempting to download PDFs.
# It performs the following tasks:
# 1. Checks the accessibility and validity of URLs using HTTP requests.
# 2. Ensures that the URL points to a PDF file (by checking the file extension).
# 3. Provides functions to extract valid URLs from the primary or alternative columns.
# This ensures that only valid URLs are processed, reducing errors in the download step.

# validate_urls.py

import requests
import pandas as pd  # Retained for main workflow consistency

# Function to validate a URL by checking its accessibility and content type
def validate_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=2)  # Changed to GET for more thorough validation
        # Check for a successful response and that the URL ends in '.pdf'
        return response.status_code == 200 and response.headers.get('Content-Type', '').lower().startswith('application/pdf')
    except requests.RequestException:
        return False

# Function to retrieve a valid URL from primary or alternative column
def get_valid_url(row, primary_col, alternative_col):
    primary_url = row.get(primary_col)
    alternative_url = row.get(alternative_col)

    if pd.notna(primary_url) and validate_url(primary_url):  # Use pd.notna to handle NaN values in DataFrame
        return primary_url
    if pd.notna(alternative_url) and validate_url(alternative_url):
        return alternative_url

    return None

