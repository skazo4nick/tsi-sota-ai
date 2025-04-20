import os
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from dotenv import load_dotenv

"""
This test uses the native Backblaze B2 SDK (b2sdk) to connect to your B2 bucket.
It:
1. Loads B2 credentials from the environment.
2. Authorizes the B2 account.
3. Retrieves the bucket by its name.
4. Lists the file names in the bucket.

Ensure you've installed b2sdk (pip install b2sdk) before running this test.
"""

def test_b2sdk_connection():
    # Load environment variables from .env file
    load_dotenv()
    
    application_key = os.getenv("B2_APPLICATION_KEY")
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    bucket_name = os.getenv("B2_BUCKET_NAME")
    
    if not all([application_key, application_key_id, bucket_name]):
        raise Exception("One or more required B2 credentials are missing from the environment.")
    
    # Set up account info and initialize the B2Api
    info = InMemoryAccountInfo()
    api = B2Api(info)
    
    try:
        # Authorize the account. Use "production" for live account.
        api.authorize_account("production", application_key_id, application_key)
        
        # Retrieve the bucket by name
        bucket = api.get_bucket_by_name(bucket_name)
        
        # List file names in the bucket
        print("Files in bucket:")
        for file_version_info, _ in bucket.ls():
            print(f" - {file_version_info.file_name}")
        
        print("\nConnection to B2 bucket (via b2sdk) successful!")
        return True
    except Exception as e:
        print(f"Error accessing bucket: {e}")
        return False

if __name__ == '__main__':
    test_b2sdk_connection()
