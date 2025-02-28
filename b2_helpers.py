import os
import logging
from dotenv import load_dotenv
from b2sdk.v2 import B2Api, InMemoryAccountInfo, Synchronizer, SyncOptions
from b2sdk.transfer.parallel import ParallelDownloader, ParallelUploader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def connect_to_b2():
    """
    Initializes and authenticates a connection to Backblaze B2.
    
    Returns:
        B2Api: An authorized B2Api client instance.
    
    Raises:
        ValueError: If B2 credentials are missing.
        Exception: If authorization fails.
    """
    load_dotenv()  # Load environment variables from a .env file

    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    if not application_key_id or not application_key:
        raise ValueError("B2 credentials (B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY) are missing.")
    
    account_info = InMemoryAccountInfo()
    b2_api = B2Api(account_info)
    try:
        b2_api.authorize_account("production", application_key_id, application_key)
        logging.info("Successfully connected to B2.")
        return b2_api
    except Exception as e:
        logging.error(f"Error connecting to B2: {e}")
        raise

def list_b2_files(b2_api, bucket_name, prefix=None):
    """
    Lists files in a specified B2 bucket, optionally filtered by a prefix.

    Args:
        b2_api (B2Api): Authenticated B2Api client instance.
        bucket_name (str): Name of the B2 bucket.
        prefix (str, optional): Prefix filter for files.

    Returns:
        list: List of file version objects.
    
    Raises:
        Exception: If bucket retrieval or listing fails.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
    except Exception as e:
        logging.error(f"Error getting bucket '{bucket_name}': {e}")
        raise

    file_list = []
    try:
        for file_version, folder_version in bucket.ls(prefix=prefix):
            if file_version:
                file_list.append(file_version)
        return file_list
    except Exception as e:
        logging.error(f"Error listing files in bucket '{bucket_name}' with prefix '{prefix}': {e}")
        raise

def upload_file_to_b2(b2_api, bucket_name, local_file_path, b2_file_path):
    """
    Uploads a local file to a specified B2 bucket.

    Args:
        b2_api (B2Api): Authenticated B2Api client instance.
        bucket_name (str): Name of the B2 bucket.
        local_file_path (str): Path to the local file.
        b2_file_path (str): Destination path/filename in the B2 bucket.

    Returns:
        Uploaded file object.
    
    Raises:
        ValueError: If file size exceeds 100MB.
        Exception: If bucket retrieval or upload fails.
    """
    # Check file size before upload
    file_size = os.path.getsize(local_file_path)
    if file_size > 100 * 1024 * 1024:  # 100MB in bytes
        raise ValueError(f"File size {file_size} exceeds maximum allowed size of 100MB")

    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
    except Exception as e:
        logging.error(f"Error getting bucket '{bucket_name}': {e}")
        raise

    try:
        uploaded_file = bucket.upload_local_file(
            local_file=local_file_path,
            file_name=b2_file_path
        )
        logging.info(f"File '{local_file_path}' uploaded to '{b2_file_path}' in bucket '{bucket_name}'.")
        return uploaded_file
    except Exception as e:
        logging.error(f"Error uploading file '{local_file_path}' to '{b2_file_path}': {e}")
        raise

def download_file_from_b2(b2_api, bucket_name, b2_file_path, local_file_path):
    """
    Downloads a file from a B2 bucket to a local path.

    Args:
        b2_api (B2Api): Authenticated B2Api client instance.
        bucket_name (str): Name of the B2 bucket.
        b2_file_path (str): File path/filename in the B2 bucket.
        local_file_path (str): Local file path to save the downloaded file.

    Returns:
        Downloaded file object.
    
    Raises:
        Exception: If bucket retrieval or download fails.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
    except Exception as e:
        logging.error(f"Error getting bucket '{bucket_name}': {e}")
        raise

    try:
        downloaded_file = bucket.download_file_by_name(file_name=b2_file_path)
        with open(local_file_path, "wb") as f:
            f.write(downloaded_file.content)
        logging.info(f"File '{b2_file_path}' downloaded to '{local_file_path}'.")
        return downloaded_file
    except Exception as e:
        logging.error(f"Error downloading file '{b2_file_path}' to '{local_file_path}': {e}")
        raise

def delete_b2_file(b2_api, bucket_name, b2_file_path):
    """
    Deletes a file from a specified B2 bucket.

    Args:
        b2_api (B2Api): Authenticated B2Api client instance.
        bucket_name (str): Name of the B2 bucket.
        b2_file_path (str): File path/filename in the B2 bucket to delete.

    Returns:
        Deleted file object.
    
    Raises:
        Exception: If bucket retrieval or deletion fails.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
    except Exception as e:
        logging.error(f"Error getting bucket '{bucket_name}': {e}")
        raise

    try:
        deleted_file = bucket.delete_file_version(file_name=b2_file_path, file_id=None)
        logging.info(f"File '{b2_file_path}' deleted from bucket '{bucket_name}'.")
        return deleted_file
    except Exception as e:
        logging.error(f"Error deleting file '{b2_file_path}': {e}")
        raise

def get_b2_file_metadata(b2_api, bucket_name, b2_file_path):
    """
    Retrieves the metadata for a file in a B2 bucket.

    Args:
        b2_api (B2Api): Authenticated B2Api client instance.
        bucket_name (str): Name of the B2 bucket.
        b2_file_path (str): File path/filename in the B2 bucket.

    Returns:
        File metadata object.
    
    Raises:
        Exception: If bucket retrieval or metadata retrieval fails.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
    except Exception as e:
        logging.error(f"Error getting bucket '{bucket_name}': {e}")
        raise

    try:
        file_info = bucket.get_file_info_by_name(file_name=b2_file_path)
        return file_info
    except Exception as e:
        logging.error(f"Error getting metadata for file '{b2_file_path}': {e}")
        raise

def sync_b2_with_local(b2_api, bucket_name, local_dir_path, b2_prefix):
    """
    Synchronizes a local directory with a specified path in a B2 bucket.

    Args:
        b2_api (B2Api): Authenticated B2Api client instance.
        bucket_name (str): Name of the B2 bucket.
        local_dir_path (str): Local directory to synchronize.
        b2_prefix (str): Prefix/path in the B2 bucket for synchronization.
    
    Raises:
        Exception: If synchronization fails.
    """
    try:
        bucket = b2_api.get_bucket_by_name(bucket_name)
    except Exception as e:
        logging.error(f"Error getting bucket '{bucket_name}': {e}")
        raise

    synchronizer = Synchronizer(b2_api, ParallelUploader(), ParallelDownloader())
    sync_options = SyncOptions()
    try:
        synchronizer.sync_folders(
            sync_options=sync_options,
            source_folder=local_dir_path,
            dest_folder=bucket,
            dest_folder_prefix=b2_prefix
        )
        logging.info(f"Successfully synchronized '{local_dir_path}' with bucket '{bucket_name}' at prefix '{b2_prefix}'.")
    except Exception as e:
        logging.error(f"Error synchronizing '{local_dir_path}' with bucket '{bucket_name}': {e}")
        raise
