import pytest
from unittest.mock import Mock, patch
from validate_urls import validate_url, get_valid_url
import pandas as pd

# Path to your lightweight test file
excel_file_path = "../data/test.xlsx"

@pytest.fixture
def sample_data():
    """
    Load the Excel file and return a DataFrame.
    This will be used in tests as sample input.
    """
    return pd.read_excel(excel_file_path)

@patch("validate_urls.requests.get")
def test_validate_url_success(mock_get, sample_data):
    """
    Test validate_url with valid and invalid URLs from the Excel file.
    """
    # Mock specific URL behavior
    def mock_get_side_effect(url, *args, **kwargs):
        mock_response = Mock()
        if "invalid" in url:  # Simulate invalid URLs
            mock_response.status_code = 404
            mock_response.headers = {}
        else:  # Simulate valid URLs
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/pdf"}
        return mock_response

    mock_get.side_effect = mock_get_side_effect

    valid_urls = sample_data["Pdf_URL"].dropna().tolist()
    for url in valid_urls:
        is_valid = validate_url(url)
        expected_valid = not "invalid" in url  # Expected outcome
        print(f"Testing URL: {url} -> {is_valid}, Expected: {expected_valid}")
        assert is_valid == expected_valid

@patch("validate_urls.requests.get")
def test_get_valid_url_primary(mock_get, sample_data):
    """
    Test get_valid_url with rows where the primary URL (Pdf_URL) is valid or invalid.
    """
    # Mock specific URL behavior
    def mock_get_side_effect(url, *args, **kwargs):
        mock_response = Mock()
        if "invalid" in url:  # Simulate invalid URLs
            mock_response.status_code = 404
            mock_response.headers = {}
        else:  # Simulate valid URLs
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "application/pdf"}
        return mock_response

    mock_get.side_effect = mock_get_side_effect

    primary_col = "Pdf_URL"
    alternative_col = "Report Html Address"
    for index, row in sample_data.iterrows():
        valid_url = get_valid_url(row, primary_col, alternative_col)
        # Determine expected URL
        if "invalid" in str(row[primary_col]):
            expected_url = row[alternative_col] if pd.notna(row[alternative_col]) else None
        else:
            expected_url = row[primary_col]
        print(f"Row {index}: Primary: {row[primary_col]}, Fallback: {row[alternative_col]}, Result: {valid_url}, Expected: {expected_url}")
        assert valid_url == expected_url
