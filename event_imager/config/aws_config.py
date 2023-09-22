import boto3
from env import config

s3_client = boto3.client('s3',
                         region_name=config['aws_region'],
                         aws_access_key_id=config['aws_access_key_id'],
                         aws_secret_access_key=config['aws_secret_access_key'])
