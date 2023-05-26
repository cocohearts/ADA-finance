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



"""
DOCUMENTATION

import * from this file

execute pipeline_setup.py

run call_model
"""

@component(packages_to_install=["google-cloud-storage","numpy","pandas==0.25.3","scikit-learn","fsspec","gcsfs","matplotlib","statsmodels","datetime","joblib","keras","pathlib","tensorflow"])
def predict_batch(gcs_bucket: str, date: str, prediction_dates: list, prediction_data: list, output_path: str, model_name: str, context_filenames: list):
    import joblib
    from google.cloud import storage
    import pandas as pd
    import numpy as np
    import tensorflow
    import keras

    bucket = storage.Client().bucket(gcs_bucket)
    
    for context_filename, context_filepath in context_filenames:
        blob = bucket.blob(context_filename)
        blob.download_to_filename(context_filename)

    # # Load ML model from GCS
    # storage_client = storage.Client()
    # bucket = storage_client.bucket(gcs_bucket)
    # blobs = bucket.list_blobs(prefix="model.sav/")
    # for blob in blobs:
    #     blob.download_to_filename(filename)
    from pathlib import Path
        
    # bucket_name = 'your-bucket-name'
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
    
    import neural_net
    import load
    import preprocessing

    model = neural_net.neural_net(keras.models.load_model("model.sav"))

    period_prediction_dates = pd.PeriodIndex([pd.Period(date_str, freq='M') for date_str in prediction_dates])
    prediction_y = pd.DataFrame(prediction_data, index=period_prediction_dates)
    # Predict for the next 5 days
    prediction = model.predict_future(prediction_y,60)
    prediction = pd.DataFrame(prediction)

    # Store prediction to GCS
    bucket.blob(output_path).upload_from_string(prediction.to_csv(index=False), 'text/csv')

    print(f"Prediction file path: {output_path}")

def call_model():
    api_client = AIPlatformClient(project_id=project_id, region=region)

    response = api_client.create_run_from_job_spec(
        job_spec_path=f"{predict_pipeline_name}.json",
        pipeline_root=pipeline_root_path,
        enable_caching=False
    )
    sleep(360)
    with open("./static/prediction.txt","w") as f:
        f.write(read(output_path))

if __name__=="__main__":
    exec(open("pipeline_setup.py").read())
    call_model()