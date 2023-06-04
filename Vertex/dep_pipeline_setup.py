sp500_history = yf.Ticker('^GSPC').history(period='15d')['Close']
prediction_data = list(sp500_history)

date = str(datetime.now().date())

ticker = "TRIP"
f = 60

data = pd.read_csv("data/" + ticker + "_data.csv")
data = data.set_index(pd.to_datetime(data["date"]))
data = data.asfreq('B')
data = data.fillna(method="ffill")
_, y_other = preprocessing(data)
# assert len(y_other) > 24, "Not enough data for prediction"
first = y_other[0]
last = y_other[-1]
y_other = to_percent(y_other)
y_other.index = y_other.index.to_series().astype(str)

prediction_data = list(y_other.values)
prediction_dates = y_other.index.tolist()

# y_future = model.predict_future(y_other, f)

print(prediction_dates,prediction_data)

@pipeline(
    name="predictionpipeline",
    description="Prediction Pipeline",
    pipeline_root=pipeline_root_path,
)
def pipeline():
    predict_batch(
        gcs_bucket,
        "test",
        prediction_dates,
        prediction_data,
        output_path,
        model_name,
        dependencies
    )

compiler.Compiler().compile(
    pipeline_func=pipeline, package_path=f"{predict_pipeline_name}.json"
)