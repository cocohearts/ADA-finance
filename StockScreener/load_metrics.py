import pandas as pd
from stock import *
from stockscreener import *
import pickle

def load_metrics():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    companies = [Stock(symbol=sp500["Symbol"][i], name=sp500["Security"][i]) for i in range(len(sp500))]
    for index, company in enumerate(companies):
        if index % 10 == 0:
            print(f"Getting metrics for {index}th company")
        companies[index] = add_metrics(company)
    print("Done getting metrics")

    pickle.dump(companies, open("StockScreener/companies.p", "wb"))


load_metrics()
