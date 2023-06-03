from google.cloud import storage
from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
from Vertex.directory_parameters import *
from Vertex.write_data import *
from time import sleep
import yfinance as yf
import numpy as np
from datetime import datetime
import pandas as pd
from pathlib import Path

def f():
    directory = "model.sav/"
        # dl_dir = 'your-local-directory/'

    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blobs = bucket.list_blobs(prefix=directory)  # Get list of files
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = "/".join(file_split[0:-1])
        Path(directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(blob.name)