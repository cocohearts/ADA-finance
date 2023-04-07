import pandas as pd
import datetime

def load():
    now = datetime.datetime.now()
    SPX = pd.read_csv('SPX.csv')
    SPX = SPX.set_index(pd.to_datetime(SPX["Date"]))
    SPX = SPX.asfreq('B')
    print("Missing datapoints:", SPX.isna().sum().sum())
    SPX = SPX.fillna(method="ffill")
    print("Loaded data in", (datetime.datetime.now()-now).microseconds / 1000, "milliseconds")
    return SPX
