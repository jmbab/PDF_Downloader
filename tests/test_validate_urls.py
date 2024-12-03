import pytest
import pandas as pd
import sys
import os

# Add the src directory to sys.path before importing project modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from validate_urls import validate_url, get_valid_url  # Import after modifying sys.path

# Path to the data Excel file
excel_file_path = "../data/GRI_2017_2020.xlsx"

@pytest.fixture
def sample_data():
    """
    Load the Excel file and return a sample row.
    This will be used in tests as a sample input.
    """
    df = pd.read_excel(excel_file_path)
    return df.iloc[0]  # Use the first row as a sample

def test_validate_url_success(sample_data):
    """
    Test validate_url with a valid URL from the Excel file.
    """
    url = sample_data["Pdf_URL"]
    if pd.notna(url):  # Ensure the URL exists and is not NaN
        assert validate_url(url) is True

def test_validate_url_failure():
    """
    Test validate_url with an invalid URL.
    """
    assert validate_url("https://www.invalid-url.com/file.pdf") is False

def test_get_valid_url(sample_data):
    """
    Test get_valid_url with a sample row.
    """
    primary_col = "Pdf_URL"
    alternative_col = "Report Html Address"
    valid_url = get_valid_url(sample_data, primary_col, alternative_col)

    # Assert the valid URL is the correct one based on primary or alternative column
    assert valid_url == (
        sample_data[primary_col]
        if pd.notna(sample_data[primary_col])
        else sample_data[alternative_col]
    )
