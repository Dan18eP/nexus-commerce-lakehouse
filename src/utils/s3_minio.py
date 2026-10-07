from minio import Minio
import os
from src.utils.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, S3_BUCKET

def get_minio_client(endpoint=None):
    ep = endpoint or MINIO_ENDPOINT
    # Limpiar prefijo http si viene en endpoint
    if ep.startswith("http://"):
        ep = ep.replace("http://", "")
    elif ep.startswith("https://"):
        ep = ep.replace("https://", "")
    
    return Minio(
        ep,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

def ensure_bucket_exists(bucket_name=S3_BUCKET):
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    return client

def upload_file_to_s3(local_path: str, object_name: str, bucket_name=S3_BUCKET):
    client = ensure_bucket_exists(bucket_name)
    client.fput_object(bucket_name, object_name, local_path)
    return f"s3://{bucket_name}/{object_name}"
