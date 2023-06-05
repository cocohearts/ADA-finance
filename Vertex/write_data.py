from google.cloud import storage
# from Forecasting.preprocessing import preprocessing
from directory_parameters import *

local_filename = "test.txt"
model_blobname = model_name

def write(blobname,local_path):
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(blobname)

    blob.upload_from_filename(local_path)

def upload_model():
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(model_blobname)

    blob.upload_from_filename(model_filepath)

def read(filename):
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(filename)

    with blob.open("r") as f:
        return f.read()

# def read(filename):
#     bucket = storage.Client().bucket(gcs_bucket)
#     blob = bucket.blob(filename)
#     with blob.open("r") as f:
#         return f.read(output_path)

# def read(filename):
#     """Write and read a blob from GCS using file-like IO"""
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(gcs_bucket)
#     blob = bucket.blob(filename)
#     blob.download_to_filename("mymodel.sav")

# write(predict_file,local_filename)

# write(context_filename1,context_filepath1)
# write(context_filename2,context_filepath2)
# for context_filename, context_filepath in dependencies:
#     write(context_filename,context_filepath)
# read(model_name)
# upload_model()
# read(output_path)

# obj = read(context_filename1)
# print(type(obj))
# print(obj)
# exec(obj)
# print(type(preprocessing))