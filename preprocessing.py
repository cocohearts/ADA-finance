import pandas as pd
import datetime
now = datetime.datetime.now()
SPX = pd.read_csv('SPX.csv')
print(SPX.isna().sum().sum())
print((datetime.datetime.now()-now).microseconds)