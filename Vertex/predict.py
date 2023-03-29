from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
from directory_parameters import *

predict_pipeline_name = "S&P_predict_pipeline"

@component(packages_to_install=["google-cloud-storage","pandas","scikit-learn==0.21.3","fsspec","gcsfs","matplotlib","statsmodels","datetime","joblib"])
def predict_batch(gcs_bucket: str, predict_file: str, model_path: str, output_path: str, model_name: str, project_id: str, model_blobname: str, context_filenames: list):
    # from sklearn.externals import joblib
    import joblib
    from google.cloud import storage
    import pandas as pd
    from io import StringIO

    def read(filename):
        bucket = storage.Client().bucket(gcs_bucket)
        blob = bucket.blob(filename)
        with blob.open("r") as f:
            return f.read()

    model_local_uri = model_name
    gcs_client = storage.Client(project=project_id)
    bucket = gcs_client.bucket(gcs_bucket)

    # Load predict data from GCS to pandas
    dataframe = pd.read_csv(StringIO(read(predict_file)), sep=",", header=None)

    for context_filename, context_filepath in context_filenames:
        exec(read(context_filename))

    # Load ML model from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    model_file = bucket.blob(model_blobname)
    model_file.download_to_filename(model_local_uri)
    loaded_model = joblib.load(model_local_uri)

    # Predict
    prediction = loaded_model.predict(dataframe)
    prediction = pd.DataFrame(prediction)

    # Store prediction to GCS
    bucket.blob(output_path).upload_from_string(prediction.to_csv(index=False), 'text/csv')

    print(f"Prediction file path: {output_path}")

@pipeline(
    name="predictionpipeline",
    description="Prediction Pipeline",
    pipeline_root=pipeline_root_path,
)
def pipeline():
    predict_batch(
        gcs_bucket,
        predict_file,
        f"{train_pipeline_name}/artefacts/{model_name}",
        f"{predict_pipeline_name}/artefacts/prediction.csv",
        model_name,
        project_id,
        model_name,
        dependencies
    )

compiler.Compiler().compile(
    pipeline_func=pipeline, package_path=f"{predict_pipeline_name}.json"
)

def call_model():
    api_client = AIPlatformClient(project_id=project_id, region=region)

    response = api_client.create_run_from_job_spec(
        job_spec_path=f"{predict_pipeline_name}.json",
        pipeline_root=pipeline_root_path
    )

call_model()