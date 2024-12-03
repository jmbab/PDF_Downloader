import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to sys.path before importing project modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from download_pdf import download_pdf  # Import after modifying sys.path
import requests  # Import requests for the HTTPError exception

@patch("download_pdf.requests.get")
def test_download_pdf_success(mock_get):
    """
    Test download_pdf with a mocked valid URL and BRnum.
    """
    # Mock the response for a successful download
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"PDF content"
    mock_get.return_value = mock_response

    url = "https://example.com/sample.pdf"  # Placeholder URL
    brnum = "BR0001"
    download_folder = "downloads"

    result = download_pdf(url, brnum, download_folder)
    assert result == "Downloaded"

@patch("download_pdf.requests.get")
def test_download_pdf_failure(mock_get):
    """
    Test download_pdf with a mocked invalid URL.
    """
    # Mock the response for a failed download
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.content = b""  # Empty byte string to simulate no content
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error: Not Found for url")
    mock_get.return_value = mock_response

    url = "https://invalid-url.com/sample.pdf"
    brnum = "BR0002"
    download_folder = "downloads"

    result = download_pdf(url, brnum, download_folder)
    assert result == "Not downloaded"

 
    
'''
DIDACTIC COMMENT:
Expanded Explanation of @patch

1) Purpose:

@patch is a decorator from the unittest.mock library used to replace real objects in your code with mock objects during a test.
It ensures tests are isolated and do not rely on external factors like the internet or file systems.

2) How It Works:

@patch("module_name.function_name") tells the test to replace function_name in module_name with a mock object.
The mock object can simulate behaviors like returning specific values or raising exceptions.

3) Benefits:

Prevents real network requests during testing.
Allows you to test error scenarios without relying on real-world failures.
Speeds up tests by avoiding delays like network latency.

4) In This Code:

@patch("download_pdf.requests.get") replaces requests.get with a mock in the download_pdf module.
The mock_get argument in the test function is the mock object for requests.get, which you can control to simulate different behaviors.
'''
