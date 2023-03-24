project_id = "ada-cloud-compute"
gcs_bucket = "ada_finance_dataset"
region = "us-central1"
train_pipeline_name = "S&P_train_pipeline"
pipeline_root_path = f"gs://{gcs_bucket}/{train_pipeline_name}"

predict_file = "prediction_data.txt"

# model_name = "../Forecasting/model.sav"
model_name = "hi"