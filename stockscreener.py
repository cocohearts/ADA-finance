import stockscreener_functions
from stock import Stock
import finnhub
import pandas as pd
import time


finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")


sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
sp010 = sp500[:10]
companies = dict(zip(sp010["Symbol"], sp010["Security"]))
# print(companies)

for symbol in companies.keys():
    try:
        data = finnhub_client.company_basic_financials(symbol, metric='all')
    except finnhub.FinnhubAPIException:
        print("sleeping")
        time.sleep(60)
        data = finnhub_client.company_basic_financials(symbol, metric='all')

    metrics = data["metric"]
    companies[symbol] = stockscreener_functions.insert_metrics(metrics)

# Price/earnings, Price/book, Revenue growth in 5 years, Price/sales
criteria = {'PE': ('<', 10), 'PB': ('<=', 0.7), 'RG5Y': ('>=', 10), 'PS': ('<', 1)}



