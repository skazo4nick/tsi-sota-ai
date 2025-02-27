import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

def test_b2_connection():
    # Load environment variables from .env file
    load_dotenv()

    b2_key = os.getenv("B2_APPLICATION_KEY")
    b2_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    endpoint_url = os.getenv("B2_S3_ENDPOINT")
    bucket_name = os.getenv("B2_BUCKET_NAME")

    if not all([b2_key, b2_key_id, endpoint_url, bucket_name]):
        raise Exception("One or more required B2 credentials are missing from the environment.")

    # Create an S3 client configured for Backblaze B2
    s3 = boto3.client(
        's3',
        aws_access_key_id=b2_key_id,
        aws_secret_access_key=b2_key,
        endpoint_url=endpoint_url
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
