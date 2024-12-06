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
import signal
import sys
import threading

# Lock to prevent race conditions (in writing metadata to Metadata2024.xlsx and avoiding file corruption)
metadata_lock = threading.Lock()

# Global variable to track interruptions (with CTRL + C)
interrupted = False


def handle_interrupt(signum, frame):
    """
    Handle SIGINT (Ctrl+C) interruptions gracefully.
    """
    global interrupted
    interrupted = True
    print("\nProcess interrupted! Safely closing files...")
    sys.exit(1)  # Exit the script immediately (with CTRL + C)


# Register the interrupt handler
signal.signal(signal.SIGINT, handle_interrupt)


def update_metadata(brnum, status, metadata_file_path):
    """
    Updates or appends metadata entries in the Metadata2024.xlsx file.
    Ensures thread safety and graceful interruption handling.

    Args:
        brnum (str): The unique identifier for the PDF file (e.g., "BR50001").
        status (str): The status to update in the metadata file (e.g., "Downloaded").
        metadata_file_path (str): Path to the metadata Excel file.
    """
    global interrupted
    try:
        # Step 1: Lock the critical section
        with metadata_lock:
            # Step 2: Load or create the metadata DataFrame
            if os.path.exists(metadata_file_path):
                metadata_df = pd.read_excel(metadata_file_path, engine="openpyxl")
                print(f"Metadata file loaded. Existing entries: {len(metadata_df)}")
            else:
                metadata_df = pd.DataFrame(columns=["BRnum", "pdf_downloaded"])
                print("Metadata file does not exist. Creating a new one.")

            # Step 3: Update existing BRnum or append a new one
            if brnum in metadata_df["BRnum"].values:
                metadata_df.loc[metadata_df["BRnum"] == brnum, "pdf_downloaded"] = status
                print(f"Updated existing entry for BRnum {brnum}.")
            else:
                new_row = {"BRnum": brnum, "pdf_downloaded": status}
                metadata_df = pd.concat([metadata_df, pd.DataFrame([new_row])], ignore_index=True)
                print(f"Added new entry for BRnum {brnum}.")

            # Step 4: Sort by BRnum in ascending order
            metadata_df = metadata_df.sort_values(by="BRnum").reset_index(drop=True)
            print("Sorted metadata entries by BRnum.")

            # Step 5: Save the metadata back to the file
            if not interrupted:  # Ensure no interruption before saving
                with pd.ExcelWriter(metadata_file_path, engine="openpyxl", mode="w") as writer:
                    metadata_df.to_excel(writer, index=False)
                print(f"Metadata successfully saved and updated for BRnum {brnum} with status: {status}")
                print(f"Total entries now: {len(metadata_df)}")

    except Exception as e:
        print(f"Error updating metadata for BRnum {brnum}: {e}")

    finally:
        # Step 6: Cleanup temporary files (if any)
        temp_file_path = os.path.join(
            os.path.dirname(metadata_file_path), f"~${os.path.basename(metadata_file_path)}"
        )
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Remove temporary files if they exist
            print(f"Temporary file {temp_file_path} removed.")
        print("Process completed or safely terminated.")
