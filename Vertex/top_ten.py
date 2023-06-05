from os import listdir
import matplotlib.pyplot as plt
import pandas as pd

import os
import glob

prediction_names = listdir('predictions/')
value_ticker_arr = []

for prediction_filename in prediction_names:
    if prediction_filename[-3:] != "csv":
        continue
    ticker = prediction_filename[:-9]
    try:
        df = pd.read_csv(f'predictions/{prediction_filename}')
    except:
        continue

    ticker = prediction_filename[:-15]
    values = list(df['close'])
    growth = values[-1]/values[-25]

    value_ticker_arr.append((growth,ticker))

value_ticker_arr.sort(reverse=True)
tickers = [pair[1] for pair in value_ticker_arr[:10]]
pd.DataFrame(tickers).to_csv("predictions/top10.txt",index=False)