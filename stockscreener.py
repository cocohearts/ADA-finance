import stockscreener_functions
from stock import Stock
import finnhub
import pandas as pd
import time


def get_metrics(c):
    symbol = c.symbol
    try:
        data = finnhub_client.company_basic_financials(symbol, metric='all')
    except finnhub.FinnhubAPIException:
        print("sleeping")
        time.sleep(60)
        data = finnhub_client.company_basic_financials(symbol, metric='all')

    c.metrics = stockscreener_functions.insert_metrics(data, criteria, translations)
    return c

def find_matches(stocks, criteria):
    for c in stocks:
        symbol = c.symbol
        if stockscreener_functions.match_conditions(criteria, c.metrics):
            try:
                profile = finnhub_client.company_profile2(symbol=symbol)
            except finnhub.FinnhubAPIException:
                print("sleeping")
                time.sleep(60)
                profile = finnhub_client.company_profile2(symbol=symbol)

            c.industry = profile["finnhubIndustry"]
            c.market_cap = profile["marketCapitalization"]

            try:
                c.price = finnhub_client.quote(symbol=symbol)
            except finnhub.FinnhubAPIException:
                print("sleeping")
                time.sleep(60)
                c.price = finnhub_client.company_profile2


finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
companies = [Stock(symbol=sp500["Symbol"][i], name=sp500["Security"][i]) for i in range(len(sp500))]
for c in companies:
    c = get_metrics(c)
# print(companies)

# Price/earnings, Price/book, Revenue growth in 5 years, Price/sales
criteria = {'PE': ('<', 10), 'PB': ('<=', 0.7), 'RG5Y': ('>=', 10), 'PS': ('<', 1)}
translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM'}

