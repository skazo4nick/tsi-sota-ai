import pytest
from unittest.mock import Mock, patch
import logging
import os
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from b2sdk.sync import Synchronizer, SyncOptions
from b2sdk.transfer.parallel import ParallelDownloader, ParallelUploader
from b2_helpers import (
    connect_to_b2,
    list_b2_files,
    upload_file_to_b2,
    download_file_from_b2,
    delete_b2_file,
    get_b2_file_metadata,
    sync_b2_with_local
)

@pytest.fixture
def mock_b2_api():
    return Mock(spec=B2Api)

@pytest.fixture
def mock_bucket():
    return Mock()

@pytest.fixture
def mock_synchronizer():
    return Mock(spec=Synchronizer)

def test_connect_to_b2_success(monkeypatch):
    # Arrange
    monkeypatch.setenv("B2_APPLICATION_KEY_ID", "test_key_id")
    monkeypatch.setenv("B2_APPLICATION_KEY", "test_key")
    mock_b2_api = Mock()
    with patch("b2_helpers.B2Api", return_value=mock_b2_api):
        # Act
        result = connect_to_b2()
        # Assert
        assert result == mock_b2_api
        mock_b2_api.authorize_account.assert_called_once_with(
            "production", "test_key_id", "test_key"
        )

def test_connect_to_b2_missing_credentials(monkeypatch):
    # Arrange
    monkeypatch.delenv("B2_APPLICATION_KEY_ID", raising=False)
    monkeypatch.delenv("B2_APPLICATION_KEY", raising=False)
    # Act & Assert
    with pytest.raises(ValueError):
        connect_to_b2()

def test_list_b2_files_success(mock_b2_api, mock_bucket):
    # Arrange
    mock_b2_api.get_bucket_by_name.return_value = mock_bucket
    mock_bucket.ls.return_value = [("file1", None), ("file2", None)]
    # Act
    result = list_b2_files(mock_b2_api, "test_bucket")
    # Assert
    assert len(result) == 2
    mock_b2_api.get_bucket_by_name.assert_called_once_with("test_bucket")
    mock_bucket.ls.assert_called_once_with(prefix=None)

def test_upload_file_to_b2_success(mock_b2_api, mock_bucket):
    # Arrange
    mock_b2_api.get_bucket_by_name.return_value = mock_bucket
    # Act
    upload_file_to_b2(mock_b2_api, "test_bucket", "local.txt", "remote.txt")
    # Assert
    mock_bucket.upload_local_file.assert_called_once_with(
        local_file="local.txt",
        file_name="remote.txt"
    )

def test_download_file_from_b2_success(mock_b2_api, mock_bucket):
    # Arrange
    mock_b2_api.get_bucket_by_name.return_value = mock_bucket
    mock_bucket.download_file_by_name.return_value = Mock(content=b"test content")
    # Act
    with patch("builtins.open", Mock()) as mock_open:
        download_file_from_b2(mock_b2_api, "test_bucket", "remote.txt", "local.txt")
    # Assert
    mock_bucket.download_file_by_name.assert_called_once_with(file_name="remote.txt")
    mock_open.assert_called_once_with("local.txt", "wb")

def test_delete_b2_file_success(mock_b2_api, mock_bucket):
    # Arrange
    mock_b2_api.get_bucket_by_name.return_value = mock_bucket
    # Act
    delete_b2_file(mock_b2_api, "test_bucket", "file.txt")
    # Assert
    mock_bucket.delete_file_version.assert_called_once_with(
        file_name="file.txt",
        file_id=None
    )

def test_get_b2_file_metadata_success(mock_b2_api, mock_bucket):
    # Arrange
    mock_b2_api.get_bucket_by_name.return_value = mock_bucket
    mock_file_info = Mock()
    mock_bucket.get_file_info_by_name.return_value = mock_file_info
    # Act
    result = get_b2_file_metadata(mock_b2_api, "test_bucket", "file.txt")
    # Assert
    assert result == mock_file_info
    mock_bucket.get_file_info_by_name.assert_called_once_with(file_name="file.txt")

def test_sync_b2_with_local_success(mock_b2_api, mock_bucket, mock_synchronizer):
    # Arrange
    mock_b2_api.get_bucket_by_name.return_value = mock_bucket
    with patch("b2_helpers.Synchronizer", return_value=mock_synchronizer):
        # Act
        sync_b2_with_local(mock_b2_api, "test_bucket", "local_dir", "b2_prefix")
        # Assert
        mock_synchronizer.sync_folders.assert_called_once()
