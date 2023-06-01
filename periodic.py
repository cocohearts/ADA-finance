from Vertex.new_predict import *
import schedule
# from StockScreener.load_metrics import *
from Forecasting.preprocessing import preprocessing, to_percent

def async_job(ticker):
    arr_prediction_dates = []
    arr_prediction_data = []
    arr_names = []
    for ticker in ["TRIP"]:
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
        filename = "data/" + ticker + "_data.csv"

        file_outputpath = f"{predict_pipeline_name}/artefacts/{ticker}_prediction.csv"

        prediction_data = list(y_other.values)
        prediction_dates = y_other.index.tolist()

        arr_prediction_data.append(prediction_data)
        arr_prediction_dates.append(prediction_dates)
        arr_names.append(ticker)

    @pipeline(
        name="predictionpipeline",
        description="Prediction Pipeline",
        pipeline_root=pipeline_root_path,
    )
    def pipeline():
        predict_batch(
            gcs_bucket,
            "test",
            arr_prediction_dates,
            arr_prediction_data,
            file_outputpath,
            model_name,
            dependencies,
            filename
        )

    compiler.Compiler().compile(
        pipeline_func=pipeline, package_path=f"{predict_pipeline_name}.json"
    )
    call_model()

    # load_metrics()

# schedule.every().day.do(async_job)
async_job(1)