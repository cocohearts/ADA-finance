import pandas as pd

def get_tickers():
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return list(sp500['Symbol'])