import pandas as pd
from StockScreener.stock import *
from StockScreener.stockscreener import *

def load_metrics():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    companies = [Stock(symbol=sp500["Symbol"][i], name=sp500["Security"][i]) for i in range(len(sp500))]
    for i in range(len(companies)):
        if i % 10 == 0:
            print(f"Getting metrics for {i}th company")
        companies[i] = get_metrics(companies[i])
    print("Done getting metrics")

    pickle.dump(companies, open("companies.p", "wb"))

if __name__ == "__main__":
    load_metrics()