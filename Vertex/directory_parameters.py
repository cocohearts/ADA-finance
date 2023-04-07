project_id = "ada-cloud-compute"
gcs_bucket = "ada_finance_dataset"
region = "us-central1"
train_pipeline_name = "S&P_train_pipeline"
predict_pipeline_name = "S&P_predict_pipeline"
pipeline_root_path = f"gs://{gcs_bucket}/{train_pipeline_name}"

predict_file = "prediction_data.txt"

model_name = "SP_model.sav"
context_filename1 = "preprocessing.py"
context_filename2 = "hybrid.py"

context_filepath1 = "../Forecasting/preprocessing.py"
context_filepath2 = "../Forecasting/hybrid.py"

output_path = f"{predict_pipeline_name}/artefacts/prediction.csv"

dependencies = [
    ("context.py","../Forecasting/context.py"),
    ("hybrid.py","../Forecasting/hybrid.py"),
    ("preprocessing.py","../Forecasting/preprocessing.py"),
    ("neural_net.py","../Forecasting/neural_net.py"),
    ("linear_regression.py","../Forecasting/linear_regression.py")
]

model_filepath = "../Forecasting/model.sav"
# model_name = "hi"