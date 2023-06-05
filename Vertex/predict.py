from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
from directory_parameters import *
from write_data import *
from time import sleep
import numpy as np
from datetime import datetime
import pandas as pd
from os import listdir
import matplotlib.pyplot as plt
from get_tickers import get_tickers

"""
DOCUMENTATION

export GOOGLE_APPLICATION_CREDENTIALS="Vertex/ada-cloud-compute-f7feeb229766.json"
then execute this file
"""

@component(packages_to_install=["google-cloud-storage","numpy","pandas==0.25.3","scikit-learn","fsspec","gcsfs","matplotlib","statsmodels","datetime","joblib","keras","pathlib","tensorflow","datetime","python-dateutil"])
def predict_batch(gcs_bucket: str, file_names: list, output_names: list, context_file_names: list):
    import joblib
    from google.cloud import storage
    import pandas as pd
    import numpy as np
    import tensorflow
    import keras
    import datetime as dt
    from dateutil.relativedelta import relativedelta

    bucket = storage.Client().bucket(gcs_bucket)
    
    for context_filename, context_filepath in context_file_names:
        blob = bucket.blob(context_filename)
        blob.download_to_filename(context_filename)

    # # Load ML model from GCS
    from pathlib import Path
        
    # bucket_name = 'your-bucket-name'
    model_directory = "model.sav/"

    blobs = bucket.list_blobs(prefix=model_directory)  # Get list of files
    for blob in blobs:
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        model_directory = "/".join(file_split[0:-1])
        Path(model_directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(blob.name)
    
    import neural_net
    import load
    from preprocessing import to_percent, to_values, preprocessing

    model = neural_net.neural_net(keras.models.load_model("model.sav"))

    print("model loaded")

    for index in range(len(file_names)):
        filename = file_names[index]
        print("processing",filename)
        outputname = output_names[index]
        blob = bucket.blob(f"data/{filename}")
        blob.download_to_filename(filename)
        
        data = pd.read_csv(filename)[['date','close']]
        if data.size == 0:
            continue
        data = data.set_index(pd.to_datetime(data["date"]))
        data = data.asfreq('B')
        data = data.fillna(method="ffill")
        y_other = data["close"]
        y_other = y_other.groupby(pd.PeriodIndex(y_other.index, freq="M")).mean()
        if len(y_other) <= 24:
            continue
        last = y_other[-1]
        percentage_y_other = to_percent(y_other)
        print("loading done")
        prediction = model.predict_future(percentage_y_other,60)
        print("prediction done")
        y_future = to_values(last, prediction)

        data = data.asfreq('M')
        data = data.fillna(method="ffill")[['close']]

        finalprediction = pd.DataFrame()
        finalprediction['close'] = y_future

        today=dt.date.today()
        prediction_end = today + relativedelta(months=+61)
        pidx=pd.period_range(start=today,end=prediction_end,freq='M')
        finalprediction.set_index(pidx[1:])

        prediction = pd.concat([data,finalprediction])

        bucket.blob(f"predictions/{outputname}").upload_from_string(prediction.to_csv(index=True), 'text/csv')
        print(filename,"processed")

# file_names = listdir('data/')
tickers = get_tickers()

output_names = [ticker+"_prediction.csv" for ticker in tickers]
file_names = [ticker+"_data.csv" for ticker in tickers]
outputpaths = [f"predict_pipeline/artefacts/{outputname}" for outputname in output_names]

@pipeline(
    name="predictionpipeline",
    description="Prediction Pipeline",
    pipeline_root=pipeline_root_path,
)
def pipeline():
    predict_batch(
        gcs_bucket,
        file_names,
        output_names,
        dependencies
    )

compiler.Compiler().compile(
    pipeline_func=pipeline, package_path=f"{predict_pipeline_name}.json"
)

api_client = AIPlatformClient(project_id=project_id, region=region)

response = api_client.create_run_from_job_spec(
    job_spec_path=f"{predict_pipeline_name}.json",
    pipeline_root=pipeline_root_path,
    enable_caching=False
)