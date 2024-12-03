# PDF Downloader and Metadata Updater

This project is a modular Python program designed to download PDF files from a list of URLs in an Excel file and update a metadata file to reflect the download status. The program adheres to the principle of **separation of concerns**, dividing responsibilities into distinct, reusable modules. This setup includes multi-threading for improved performance.

## Table of Contents
- **[Project Overview](#project-overview)**
- **[Project Structure](#project-structure)**
- **[Installation](#installation)**
- **[Usage](#usage)**
- **[Requirements](#requirements)**
- **[Modules](#modules)**
- **[Known Issues](#known-issues)**
- **[Contributing](#contributing)**

## Project Overview
The purpose of this project is to:
1. **Validate URLs**: Read URLs from a primary column, falling back on a secondary column if necessary.
2. **Download PDFs**: Save each valid PDF with a unique identifier (BRnum) as a prefix.
3. **Track Download Status**: Log the status of each PDF (Downloaded or Not Downloaded) in a separate metadata Excel file.

## Features
- **Excel Integration**: Reads URLs and metadata from Excel files using `pandas`.
- **Multithreading**: Utilizes Python's `ThreadPoolExecutor` for parallel processing of download tasks.
- **Robust Validation**: Validates URLs before attempting downloads to ensure efficiency and error handling.
- **Metadata Management**: Tracks download statuses (e.g., "Downloaded", "Not downloaded") and updates the metadata file.
- **Error Handling**: Logs errors for invalid URLs, failed downloads, or metadata update issues.

## Project Structure

```
project/
│
├── data/
│   └── GRI_2017_2020.xlsx     # Source Excel file with URLs and BRnum entries
│
├── downloads/
│   └── ...                    # Folder where downloaded PDFs will be stored
│
├── metadata/
│   └── Metadata2024.xlsx      # Metadata file tracking download statuses
│
├── src/
│   ├── pycache/	           # Compiled Python files
│   ├── download_pdf.py        # Module to handle PDF downloads
│   ├── load_excel.py          # Module to load the source Excel file
│   ├── main.py                # Main script orchestrating the workflow
│   ├── threaded_executor.py   # Multithreading for URL validation and downloads
│   ├── update_metadata.py     # Metadata update management
│   └── validate_urls.py       # URL validation module
│
└── venv/                      # Virtual environment for dependencies
```

## Installation


### Prerequisites
- Python 3.12 or higher
- `pip` (Python package installer)

### Steps
1. **Clone this repository**:

	```git clone https://github.com/jmbab/PDF_Downloader cd project```


2. **Set up a virtual environment**:

	```python -m venv venv source venv/bin/activate``` # On MacOS/Linux
	```venv\Scripts\activate``` # On Windows


3. **Install dependencies**:

	```pip install -r ../requirements.txt```


## Usage

1. **Prepare the Excel File**:
- Place the Excel file with URLs in the `data/` folder (e.g., `GRI_2017_2020.xlsx`).
- Ensure columns for `Pdf_URL` (primary) and `Report Html Address` (alternative) exist.
- Ensure a `BRnum` column contains unique identifiers for each row.

2. **Run the Main Script**:

	```python main.py```


3. **Output**:
- Downloaded PDFs will appear in the `downloads/` folder.
- Metadata updates will be reflected in `metadata/Metadata2024.xlsx`.

## Requirements
- Python 3.12 or later
- Required packages specified in `requirements.txt`:
- `pandas`
- `requests`
- `openpyxl`

## Modules

- **`main.py`**: Initializes the process and coordinates module actions.
- **`load_excel.py`**: Loads and reads the Excel file.
- **`validate_urls.py`**: Contains functions to validate URLs.
- **`download_pdf.py`**: Handles downloading and naming PDFs.
- **`update_metadata.py`**: Updates the metadata log with each PDF’s download status.
- **`threaded_executor.py`**: Manages multi-threading for faster execution.

## Known Issues

- **Slow URL Validation**: Adjusting the `timeout` parameter in `validate_urls.py` may speed up or slow down URL validation.
- **Redundant Entries in Metadata**: The script will overwrite when it encounters duplicate `BRnum` entries.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Submit a pull request with your changes.

## License
This project is open source and available under the [MIT License](LICENSE).

## Contact
For questions or feedback, feel free to reach out via email: babonneau[at]gmail[dot]com

