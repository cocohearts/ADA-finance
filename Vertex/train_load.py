from kfp.dsl import pipeline
from kfp.v2 import compiler
from kfp.v2.dsl import component
from kfp.v2.google.client import AIPlatformClient
import pandas as pd

import sys
sys.path.append('..')
from Forecasting import neural_net

project_id = "ada-cloud-compute"
gcs_bucket = "ada_finance_dataset"
region = "us-central1"
train_pipeline_name = "S&P_train_pipeline"
pipeline_root_path = f"gs://{gcs_bucket}/{train_pipeline_name}"

model_name = "S&Pmodel.joblib"

@component(packages_to_install=["google-cloud-storage","pandas","pyarrow"])
def gcs_load_data(output_gcs_bucket: str) -> str:
    from google.cloud import storage

    output_file = f"{train_pipeline_name}/artefacts/train.csv"

    dataframe = pd.DataFrame()

    # this line might be issue, not sure
    gcs_client = storage.Client(project=project_id)

    bucket = gcs_client.get_bucket(output_gcs_bucket)
    bucket.blob(output_file).upload_from_string(dataframe.to_csv(index=False), 'text/csv')

    return output_file

@component(packages_to_install=["google-cloud-storage","pandas","scikit-learn==0.21.3","fsspec","gcsfs"])
def train_model(gcs_bucket: str, train_file_path: str, model_name: str):
    from google.cloud import storage
    from sklearn import metrics
    from sklearn.externals import joblib
    import pandas as pd

    dataframe = pd.read_csv(f'gs://{gcs_bucket}/{train_file_path}')

    output_file = f"{train_pipeline_name}/artefacts/{model_name}"

    # TODO: GET STUFF FROM dataframe
    x_train = dataframe[0]
    y_train = dataframe[1]
    x_test = dataframe[2]
    y_test = dataframe[3]

    my_model = neural_net.train(x_train, y_train)

    y_pred = neural_net.test(my_model, x_test, y_test)

    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

    joblib.dump(my_model, model_name)

    bucket = storage.Client().bucket(gcs_bucket)
    blob = bucket.blob(output_file)
    blob.upload_from_filename(model_name)

    print(f"Model saved in : {output_file}")

@pipeline(
    name="trainingpipeline",
    description="Training Pipeline",
    pipeline_root=pipeline_root_path,
)
def pipeline():
    load_output = gcs_load_data(gcs_bucket)
    train_model(gcs_bucket, load_output.output, model_name)

compiler.Compiler().compile(
    pipeline_func=pipeline, package_path=f"{train_pipeline_name}.json"
)

api_client = AIPlatformClient(project_id=project_id, region=region)

response = api_client.create_run_from_job_spec(
    job_spec_path=f"{train_pipeline_name}.json",
    pipeline_root=pipeline_root_path
)