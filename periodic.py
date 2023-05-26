from Vertex.new_predict import *
import schedule
# from StockScreener.load_metrics import *
from Forecasting.preprocessing import preprocessing, to_percent

def async_job():
    exec(open("Vertex/pipeline_setup.py").read())
    call_model()

    # load_metrics()

schedule.every().day.do(async_job)