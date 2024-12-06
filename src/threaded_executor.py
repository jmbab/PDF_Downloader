# PDF DOWNLOADER & CHECKER & REGISTER FROM/TO URLs IN EXCEL FILES
# Jean M. Babonneau | Nov. 2024 | MIT License

# MODULAR PART 2: THREAD MANAGEMENT
# This module adheres to the principle of "separation of concerns" by focusing solely on
# its own task. It is designed for maintainability and reuse.
# This module handles the parallel processing of rows from the source Excel file.
# It performs the following tasks:
# 1. Uses Python's `ThreadPoolExecutor` to process multiple rows concurrently.
# 2. Validates URLs, downloads PDFs, and updates metadata for each row.
# 3. Collects results (BRnum and their statuses) to be returned to the main script.
# It ensures that the program efficiently handles large datasets by leveraging threading.

# threaded_executor.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from validate_urls import get_valid_url
from download_pdf import download_pdf
from update_metadata import update_metadata

# Function to manage threaded execution for each row
def run_threaded_execution(df, download_folder, metadata_file_path, primary_col, alternative_col, brnum_col):
    results = []  # Collect results for each BRnum and status

    with ThreadPoolExecutor() as executor:
        # Map rows to threads for processing
        future_to_row = {
            executor.submit(process_row, row, download_folder, primary_col, alternative_col, brnum_col, metadata_file_path): row
            for _, row in df.iterrows()
        }

        # Process threads and handle results
        for future in as_completed(future_to_row):
            row = future_to_row[future]
            try:
                # Get the result from the thread and collect it
                result = future.result()
                results.append(result)
                print(f"Row {row.name} with BRnum {row[brnum_col]} processed with result: {result[1]}")
            except Exception as e:
                print(f"Error processing row {row.name} with BRnum {row[brnum_col]}: {e}")

    # Sort results by BRnum for consistency
    results.sort(key=lambda x: x[0])  # Sort by BRnum
    return results


# Function to process each row and update metadata
def process_row(row, download_folder, primary_col, alternative_col, brnum_col, metadata_file_path):
    try:
        brnum = row[brnum_col]
        print(f"Processing row {row.name} with BRnum {brnum}...")

        # Validate the URL and attempt download
        url = get_valid_url(row, primary_col, alternative_col)
        if url:
            print(f"Valid URL found for BRnum {brnum}, initiating download...")
            status = download_pdf(url, brnum, download_folder)
        else:
            status = "Not downloaded"
            print(f"No valid URL found for BRnum {brnum}")

        # Safely update metadata with locking
        update_metadata(brnum, status, metadata_file_path)
        print(f"Metadata updated for BRnum {brnum} with status '{status}'")

    except KeyError as e:
        print(f"Key error processing row {row.name}: {e}")
        status = "KeyError"

    except Exception as e:
        print(f"Error processing BRnum {row.get(brnum_col, 'Unknown')}: {e}")
        status = "Processing Error"

    return brnum, status

