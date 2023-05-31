import schedule
from StockScreener import load_metrics
from StockScreener.load_metrics import *
from Vertex.predict import *

def async_job():
    exec(open("Vertex/vertex_init.py").read())
    call_model()

    load_metrics()

schedule.every().day.do(async_job)