import yfinance as yf
from os import listdir
import pandas as pd
from directory_parameters import *
from google.cloud import storage
from get_tickers import *
tickers = get_tickers()

# file_names = listdir('data/')
# tickers = [ticker[:-9] for ticker in file_names]

storage_client = storage.Client()
bucket = storage_client.bucket(gcs_bucket)

for ticker in tickers:
    tick = yf.Ticker(ticker)
    df = tick.history(period='3y',interval='1d')
    df.rename(columns={'Close':'close'},inplace=True)
    df['date'] = pd.PeriodIndex(df.index,freq='D')
    df = df[['date','close']]

    filename = f"data/{ticker}_data.csv"

    bucket.blob(filename).upload_from_string(df.to_csv(index=False),'text/csv')
    print(f'{ticker} success')