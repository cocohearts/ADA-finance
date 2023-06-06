project_id = "ada-cloud-compute"
gcs_bucket = "ada_finance_dataset"
region = "us-central1"
predict_pipeline_name = "predict_pipeline"
pipeline_root_path = f"gs://{gcs_bucket}/{predict_pipeline_name}"
endpoint_id = "132886975333007360"
project_num = "741599104884"

dependencies = [
    ("preprocessing.py","../Forecasting/preprocessing.py"),
    ("neural_net.py","../Forecasting/neural_net.py"),
]