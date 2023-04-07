sp500_history = yf.Ticker('^GSPC').history(period='15d')['Close']
prediction_data = list(sp500_history)

date = str(datetime.now().date())

@pipeline(
    name="predictionpipeline",
    description="Prediction Pipeline",
    pipeline_root=pipeline_root_path,
)
def pipeline():
    predict_batch(
        gcs_bucket,
        date,
        prediction_data,
        output_path,
        model_name,
        dependencies
    )

compiler.Compiler().compile(
    pipeline_func=pipeline, package_path=f"{predict_pipeline_name}.json"
)