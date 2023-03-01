import pandas as pd
import datetime

def load():
    now = datetime.datetime.now()
    SPX = pd.read_csv('SPX.csv')
    print(SPX.isna().sum().sum())
    print("Loaded data in", (datetime.datetime.now()-now).microseconds / 1000, "milliseconds")
    return SPX
