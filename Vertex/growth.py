from os import listdir
import matplotlib.pyplot as plt
import pandas as pd
import json

import os
import glob

from get_tickers import get_tickers

tickers = get_tickers()

prediction_names = [ticker+"_prediction.csv" for ticker in tickers]
value_ticker_arr = []
ticker_dict = dict()

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
    growth = values[-1]/values[-60]

    value_ticker_arr.append((growth,ticker))
    ticker_dict[ticker] = int((growth-1)*100)

value_ticker_arr.sort(reverse=True)
tickers = [pair[1] for pair in value_ticker_arr[:16]]
pd.DataFrame(tickers).to_csv("predictions/top.txt",index=False)

with open("predictions/growth.json", "w") as file:
    json.dump(ticker_dict,file)