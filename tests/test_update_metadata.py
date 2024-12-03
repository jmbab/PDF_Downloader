import pytest
import pandas as pd
import sys
import os

# Add the src directory to sys.path before importing project modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from update_metadata import update_metadata  # Import after modifying sys.path

@pytest.fixture
def metadata_file_path(tmp_path):
    """
    Create a temporary metadata file for testing.
    """
    temp_file = tmp_path / "test_metadata.xlsx"
    # Create a DataFrame with sample data
    df = pd.DataFrame(columns=["BRnum", "pdf_downloaded"])
    df.to_excel(temp_file, index=False)
    return str(temp_file)

def test_update_metadata_existing(metadata_file_path):
    """
    Test updating metadata for an existing BRnum.
    """
    brnum = "BR1234"
    status = "Downloaded"

    # Add an existing entry
    df = pd.DataFrame([{"BRnum": brnum, "pdf_downloaded": "Not downloaded"}])
    df.to_excel(metadata_file_path, index=False)

    # Call update_metadata
    update_metadata(brnum, status, metadata_file_path)

    # Validate the update
    updated_df = pd.read_excel(metadata_file_path)
    assert updated_df.loc[updated_df["BRnum"] == brnum, "pdf_downloaded"].values[0] == status

def test_update_metadata_new_entry(metadata_file_path):
    """
    Test updating metadata for a new BRnum.
    """
    brnum = "BR5678"
    status = "Not downloaded"

    # Call update_metadata
    update_metadata(brnum, status, metadata_file_path)

    # Validate the new entry
    updated_df = pd.read_excel(metadata_file_path)
    assert brnum in updated_df["BRnum"].values
    assert updated_df.loc[updated_df["BRnum"] == brnum, "pdf_downloaded"].values[0] == status
