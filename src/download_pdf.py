# PDF DOWNLOADER & CHECKER & REGISTER FROM/TO URLs IN EXCEL FILES
# Jean M. Babonneau | Nov. 2024 | MIT License

# MODULAR PART 4: PDF DOWNLOADER
# This module adheres to the principle of "separation of concerns" by focusing solely on
# its own task. It is designed for maintainability and reuse.
# This module is responsible for downloading PDF files from validated URLs.
# It performs the following tasks:
# 1. Makes HTTP requests to download the PDF file from the given URL.
# 2. Saves the downloaded file to the specified directory with a BRnum-prefixed filename.
# 3. Returns the download status ("Downloaded" or "Not downloaded").
# It ensures that the PDF files are downloaded reliably while handling potential errors.

# download_pdf.py

import requests
from pathlib import Path
import os

# Function to download a PDF and save it with a BRnum prefix
def download_pdf(url, brnum, download_folder):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad responses

        # Extract original PDF file name from URL
        original_name = url.split('/')[-1]
        # Construct the new file name with BRnum prefix
        new_file_name = f"{brnum}_{original_name}"
        file_path = os.path.join(download_folder, new_file_name)

        # Save the PDF to the designated folder
        with open(file_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        
        print(f"Downloaded: {new_file_name}")
        return "Downloaded"
    
    except requests.RequestException as e:
        print(f"Failed to download PDF from {url}: {e}")
        return "Not downloaded"
