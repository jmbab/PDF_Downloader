# PDF DOWNLOADER & CHECKER & REGISTER FROM/TO URLs IN EXCEL FILES
# Jean M. Babonneau | Nov. 2024 | MIT License

# MODULAR PART 3: METADATA MANAGEMENT
# This module adheres to the principle of "separation of concerns" by focusing solely on
# its own task. It is designed for maintainability and reuse.
# This module is responsible for updating the metadata file, which tracks the download status of each BRnum.
# It performs the following tasks:
# 1. Reads the existing metadata file or creates a new one if it doesn't exist.
# 2. Updates or appends the status of each BRnum based on the results of the download process.
# 3. Saves the updated metadata file back to disk.
# This ensures that the metadata file remains accurate and up-to-date throughout the process.

# update_metadata.py

import pandas as pd
import os

# Function to update or create metadata entries for each download attempt
def update_metadata(brnum, status, metadata_file_path):
    try:
        # Check if metadata file exists; if not, create a new DataFrame
        if os.path.exists(metadata_file_path):
            metadata_df = pd.read_excel(metadata_file_path)
        else:
            metadata_df = pd.DataFrame(columns=["BRnum", "pdf_downloaded"])

        # Update an existing BRnum entry or append a new one
        if brnum in metadata_df["BRnum"].values:
            metadata_df.loc[metadata_df["BRnum"] == brnum, "pdf_downloaded"] = status
        else:
            metadata_df = pd.concat([metadata_df, pd.DataFrame([{"BRnum": brnum, "pdf_downloaded": status}])], ignore_index=True)

        # Save the metadata back to the file
        metadata_df.to_excel(metadata_file_path, index=False)
        print(f"Metadata saved to: {metadata_file_path}")
    except Exception as e:
        print(f"Error updating metadata for BRnum {brnum}: {e}")

