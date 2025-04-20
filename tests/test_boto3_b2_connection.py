import os
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from dotenv import load_dotenv

"""
NOTE: This approach using boto3 to connect to Backblaze B2 S3-compatible endpoint does not work.
Multiple attempts were made with different configurations:
1. Using default path-style addressing - Failed
2. Adding region_name='eu-central' - Failed
3. Constructing endpoint URL with bucket name - Failed
4. Using signature version 's3v4' - Failed

Consider using alternative approaches or the official Backblaze B2 SDK.
"""

def test_b2_connection():
    # Load environment variables from .env file
    load_dotenv()

    b2_key = os.getenv("B2_APPLICATION_KEY")
    b2_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    base_endpoint = os.getenv("B2_S3_ENDPOINT")
    bucket_name = os.getenv("B2_BUCKET_NAME")

    if not all([b2_key, b2_key_id, base_endpoint, bucket_name]):
        raise Exception("One or more required B2 credentials are missing from the environment.")

    # Configure the S3 client for Backblaze B2
    config = Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    )

    # Construct the full endpoint URL with bucket name
    endpoint_url = f"{base_endpoint}/{bucket_name}"
    print(f"Using endpoint URL: {endpoint_url}")

    # Create an S3 client configured for Backblaze B2
    s3 = boto3.client(
        's3',
        aws_access_key_id=b2_key_id,
        aws_secret_access_key=b2_key,
        endpoint_url=endpoint_url,
        region_name='eu-central',
        config=config
    )

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        if objects:
            print("Objects in bucket:")
            for obj in objects:
                print(f" - {obj['Key']}")
        else:
            print("Bucket is empty or does not contain any objects.")
        print("\nConnection to B2 bucket successful!")
        return True
    except ClientError as e:
        print(f"Error accessing bucket: {e}")
        return False

if __name__ == '__main__':
    test_b2_connection()
