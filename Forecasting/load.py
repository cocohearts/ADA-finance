import pandas as pd
import datetime

def load(path):
    data = pd.read_csv(path)
    data = data.set_index(pd.to_datetime(data["date"]))
    data = data.asfreq('B')
    data = data.fillna(method="ffill")
    return data
