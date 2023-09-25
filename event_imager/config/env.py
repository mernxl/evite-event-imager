import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "bucket_name": os.getenv('EVENT_BUCKET_NAME'),
    "server_port": os.getenv('PORT', 9091),
    "server_host": os.getenv('HOST', 'localhost'),

    "aws_region": os.getenv('AWS_REGION'),
    "aws_access_key_id": os.getenv('AWS_ACCESS_KEY_ID'),
    "aws_secret_access_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
}
