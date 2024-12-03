import pytest
import pandas as pd
from update_metadata import update_metadata
import os

# Path to your test metadata file
metadata_file_path = "../metadata/Metadata2024.xlsx"

@pytest.fixture
def setup_metadata():
    """
    Create or clear the metadata file before running tests.
    """
    if os.path.exists(metadata_file_path):
        os.remove(metadata_file_path)
    df = pd.DataFrame(columns=["BRnum", "pdf_downloaded"])
    df.to_excel(metadata_file_path, index=False)
    return metadata_file_path

def test_update_metadata_existing(setup_metadata):
    """
    Test updating metadata for an existing BRnum entry.
    """
    metadata_file = setup_metadata
    df = pd.DataFrame([{"BRnum": "BR0001", "pdf_downloaded": "Downloaded"}])
    df.to_excel(metadata_file, index=False)

    update_metadata("BR0001", "Not downloaded", metadata_file)

    updated_df = pd.read_excel(metadata_file)
    assert updated_df.loc[updated_df["BRnum"] == "BR0001", "pdf_downloaded"].values[0] == "Not downloaded"

def test_update_metadata_new(setup_metadata):
    """
    Test updating metadata for a new BRnum entry.
    """
    metadata_file = setup_metadata
    update_metadata("BR0002", "Downloaded", metadata_file)

    updated_df = pd.read_excel(metadata_file)
    assert "BR0002" in updated_df["BRnum"].values
    assert updated_df.loc[updated_df["BRnum"] == "BR0002", "pdf_downloaded"].values[0] == "Downloaded"
