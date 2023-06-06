import pandas as pd
from StockScreener.stock import *
from StockScreener.stockscreener import *
import pickle

# This function is called every night by periodic.py to get the current metrics for each company
def load_metrics():
    # Gets the list of S&P 500 companies from Wikipedia
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    # Creates a list of Stock objects
    companies = [Stock(symbol=sp500["Symbol"][i], name=sp500["Security"][i]) for i in range(len(sp500))]
    for index, company in enumerate(companies):
        if index % 10 == 0:
            print(f"Getting metrics for {index}th company")
        # Gets the metrics for each company
        companies[index] = add_metrics(company)
    print("Done getting metrics")

    pickle.dump(companies, open("../StockScreener/companies.p", "wb"))

load_metrics()
