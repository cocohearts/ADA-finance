import yfinance as yf
import pandas as pd
from directory_parameters import *
from google.cloud import storage
from get_tickers import *

# get updated list of tickers
tickers = get_tickers()

# google cloud storage bucket object
storage_client = storage.Client()
bucket = storage_client.bucket(gcs_bucket)

for ticker in tickers:
    # fetch long-term price data from yahoofinance
    tick = yf.Ticker(ticker)
    df = tick.history(period='3y',interval='1d')
    # reformat
    df.rename(columns={'Close':'close'},inplace=True)
    df['date'] = pd.PeriodIndex(df.index,freq='D')
    df = df[['date','close']]

    filename = f"data/{ticker}_data.csv"
    
    # upload to google storage bucket
    bucket.blob(filename).upload_from_string(df.to_csv(index=False),'text/csv')
    print(f'{ticker} success')