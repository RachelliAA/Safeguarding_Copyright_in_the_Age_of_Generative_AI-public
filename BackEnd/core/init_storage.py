# core/init_s3_client.py
import boto3
from core.config import settings

_s3_client = None

def init_storage_client():
    global _s3_client # Initialize the global variable
    if _s3_client is not None:
        return  # Already initialized
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        print("S3 client initialized.")

def get_storage_client():
    if _s3_client is None:
        raise RuntimeError("S3 client not initialized.")
    return _s3_client
