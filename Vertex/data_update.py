import yfinance as yf
from os import listdir
import pandas as pd
from directory_parameters import *
from google.cloud import storage

file_names = listdir('data/')
tickers = [ticker[:-9] for ticker in file_names]

storage_client = storage.Client()
bucket = storage_client.bucket(gcs_bucket)

for ticker in tickers:
    tick = yf.Ticker(ticker)
    df = tick.history(period='24mo',interval='1mo')
    df = df.set_index(pd.PeriodIndex(df.index,freq='M'))
    df = df[['Close']]
    df.rename(columns={'Close','close'},inplace=True)
    filename = f"{ticker}_data.csv"

    bucket.blob(filename).upload_from_string(df.to_csv(index=False),'text/csv')