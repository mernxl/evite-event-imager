import os

from minio import Minio

minio_client = Minio(
    os.getenv('MINIO_ENDPOINT'),
    secure=bool(os.getenv('MINIO_USE_SSL', True)),
    region=os.environ['MINIO_REGION'],
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
)


def setup_bucket(bucket_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

