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

@component(packages_to_install=["google-cloud-storage","numpy","pandas==1.2.3","scikit-learn","fsspec","gcsfs","matplotlib","statsmodels","datetime","joblib"])
def predict_batch(gcs_bucket: str, date: str, prediction_data: list, output_path: str, model_name: str, context_filenames: list):
    import joblib
    from google.cloud import storage
    import pandas as pd
    import numpy as np

    bucket = storage.Client().bucket(gcs_bucket)
    
    for context_filename, context_filepath in context_filenames:
        blob = bucket.blob(context_filename)
        blob.download_to_filename(context_filename)

    # Load ML model from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    model_file = bucket.blob(model_name)
    model_file.download_to_filename(model_name)
    loaded_model = joblib.load(model_name)

    # Predict for the next 5 days
    prediction = loaded_model.predict([pd.to_datetime(date)],np.array(prediction_data).reshape(1,-1))
    prediction = pd.DataFrame(prediction[0])

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
    with open("prediction.txt","w") as f:
        f.write(read(output_path))

def pull_prediction():
    dataframe = pd.read_csv(filepath_or_buffer="prediction.txt")


if __name__=="__main__":
    exec(open("pipeline_setup.py").read())
    call_model()