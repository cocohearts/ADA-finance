from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
from directory_parameters import *
from write_data import *
from time import sleep
import yfinance as yf
import numpy as np
from datetime import datetime

@component(packages_to_install=["google-cloud-storage","numpy","pandas==1.2.3","scikit-learn","fsspec","gcsfs","matplotlib","statsmodels","datetime","joblib"])
def predict_batch(gcs_bucket: str, date: str, prediction_data: list, output_path: str, model_name: str):
    import joblib
    from google.cloud import storage
    import pandas as pd
    import numpy as np

    bucket = storage.Client().bucket(gcs_bucket)

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

@pipeline(
    name="predictionpipeline",
    description="Prediction Pipeline",
    pipeline_root=pipeline_root_path,
)

def call_model():
    sp500_history = yf.Ticker('^GSPC').history(period='15d')['Close']
    prediction_data = list(sp500_history)

    date = str(datetime.now().date())

    def pipeline():
        predict_batch(
            gcs_bucket,
            date,
            prediction_data,
            output_path,
            model_name,
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
    sleep(360)
    with open("prediction.txt","w") as f:
        f.write(read(output_path))

call_model()