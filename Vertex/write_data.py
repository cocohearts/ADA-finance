from google.cloud import storage
from directory_parameters import *

local_filename = "test.txt"

def write():
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(predict_file)

    blob.upload_from_filename(local_filename)

def read():
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(predict_file)

    with blob.open("r") as f:
        print(f.read())

write()
# read()