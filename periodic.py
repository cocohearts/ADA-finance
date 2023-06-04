# from Vertex.new_predict import *
import schedule
# from StockScreener.load_metrics import *
# from Forecasting.preprocessing import preprocessing, to_percent

def async_job():
    with open("predict.py","r",encoding="utf-8") as predict_source:
        exec(predict_source.read())

# schedule.every().day.do(async_job)
async_job()