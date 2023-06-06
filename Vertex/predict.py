from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
from directory_parameters import *
from get_tickers import get_tickers

# predict_batch job to send to Vertex AI Pipelines
@component(packages_to_install=["google-cloud-storage","numpy","pandas==0.25.3","scikit-learn","fsspec","gcsfs","matplotlib","statsmodels","datetime","joblib","keras","pathlib","tensorflow","datetime","python-dateutil"])
def predict_batch(gcs_bucket: str, file_names: list, output_names: list, dependencies: list):
    from google.cloud import storage
    import pandas as pd
    import numpy as np
    import tensorflow
    import keras
    import datetime as dt
    from dateutil.relativedelta import relativedelta

    # Initialize GCS bucket
    bucket = storage.Client().bucket(gcs_bucket)
    
    # Load ML model from GCS (lives in a directory)
    from pathlib import Path
    model_directory = "model.sav/"

    # List of all files in model directory
    blobs = bucket.list_blobs(prefix=model_directory)

    for blob in blobs:
        # recreate folder structure on local
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        model_directory = "/".join(file_split[0:-1])
        Path(model_directory).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(blob.name)

    # Download to virtual machine local all the required context files for model
    for context_filename, _ in dependencies:
        blob = bucket.blob(context_filename)
        blob.download_to_filename(context_filename)

    # import context files
    import neural_net
    from preprocessing import to_percent, to_values

    model = neural_net.neural_net(keras.models.load_model("model.sav"))

    # run model
    for index, filename in enumerate(file_names):
        filename = file_names[index]
        outputname = output_names[index]

        # download data files
        blob = bucket.blob(f"data/{filename}")
        blob.download_to_filename(filename)
        
        # read data
        data = pd.read_csv(filename)[['date','close']]
        if data.size == 0:
            # check for errors
            continue

        # process dataframe and rename/reset columns
        data = data.set_index(pd.to_datetime(data["date"]))
        data = data.asfreq('B')
        data = data.fillna(method="ffill")
        y_other = data["close"]
        y_other = y_other.groupby(pd.PeriodIndex(y_other.index, freq="M")).mean()
        if len(y_other) <= 24:
            # remove datasets that are too short
            continue
        last = y_other[-1]
        # normalize price data to ratio data
        percentage_y_other = to_percent(y_other)

        # feed into model
        prediction = model.predict_future(percentage_y_other,60)
        # renormalize to price values
        y_future = to_values(last, prediction)

        # crop past data to month range
        data = data.asfreq('M')
        data = data.fillna(method="ffill")[['close']]

        # concatenate prediction data to old data
        finalprediction = pd.DataFrame()
        finalprediction['close'] = y_future
        # create timeseries for prediction index
        today=dt.date.today()
        prediction_end = today + relativedelta(months=+61)
        pidx=pd.period_range(start=today,end=prediction_end,freq='M')
        finalprediction.set_index(pidx[1:])
        # concatenate
        prediction = pd.concat([data,finalprediction])

        bucket.blob(f"predictions/{outputname}").upload_from_string(prediction.to_csv(index=True), 'text/csv')
        print(filename,"processed")

# get tickers
tickers = get_tickers()

# get file lists
output_names = [ticker+"_prediction.csv" for ticker in tickers]
file_names = [ticker+"_data.csv" for ticker in tickers]

# define pipeline job
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

# compile json for pipeline job
compiler.Compiler().compile(
    pipeline_func=pipeline, package_path=f"{predict_pipeline_name}.json"
)

api_client = AIPlatformClient(project_id=project_id, region=region)

# send job
response = api_client.create_run_from_job_spec(
    job_spec_path=f"{predict_pipeline_name}.json",
    pipeline_root=pipeline_root_path,
    enable_caching=False
)