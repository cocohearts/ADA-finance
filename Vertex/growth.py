import pandas as pd
import json
from get_tickers import get_tickers

tickers = get_tickers()

prediction_names = [ticker+"_prediction.csv" for ticker in tickers]
value_ticker_arr = []
ticker_dict = dict()

for prediction_filename in prediction_names:
    if prediction_filename[-3:] != "csv":
        continue
    try:
        df = pd.read_csv(f'predictions/{prediction_filename}')
    except:
        continue

    ticker = prediction_filename[:-15]
    # values is list[int]
    values = list(df['close'])
    # ratio of final predicted price to current price
    growth = values[-1]/values[-60]

    value_ticker_arr.append((growth,ticker))
    # ticker_dict is a dictionary mapping to projected percentage growth
    ticker_dict[ticker] = int((growth-1)*100)

# sort a list of tuples by first entry, growth rate
value_ticker_arr.sort(reverse=True)
# tickers is the top 16 highest-growing stocks
tickers = [pair[1] for pair in value_ticker_arr[:16]]
# save top 16 to file
pd.DataFrame(tickers).to_csv("predictions/top.txt",index=False)

with open("predictions/growth.json", "w") as file:
    # save dictionary to file
    json.dump(ticker_dict,file)