import os

config = {
    "bucket_name": os.getenv('EVENT_BUCKET_NAME'),
    "server_port": os.getenv('SERVER_PORT', 9091),
    "server_host": os.getenv('SERVER_HOST', 'localhost')
}