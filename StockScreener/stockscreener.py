import finnhub
import time
import pickle
from StockScreener.stock import *

# Values are terms from Finnhub API documentation - see pins in Discord
translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
                'PM5Y': 'netProfitMargin5Y', 'ROE': 'roe5Y', 'DE': 'totalDebt/totalEquityAnnual',
                'CR': 'currentRatioAnnual', 'FCF': 'focfCagr5Y', 'EPSG': 'epsGrowth5Y'}

# Values are displayed on page
names = {'PE': 'Price-Earnings Ratio', 'PB': 'Price-Book Ratio', 'RG5Y': '5 Year Revenue Growth',
         'PS': 'Price-Sales Ratio', 'PM5Y': 'Profit Margin', 'ROE': 'Return on Equity',
         'DE': 'Debt-Equity Ratio', 'CR': 'Current Ratio', 'FCF': "Free Cash Flow", 'EPSG': '5 Year EPS Growth'}

finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")

# Gets list of possible industries
# We do it this way so new industries are automatically added
industries = sorted(set([company.industry for company in pickle.load(open("StockScreener/companies.p", "rb"))]))
# Basically enumerates 'industries'
industry_values = list(range(len(industries)))

# Gets data for a Stock object and adds it to the object
def add_metrics(my_stock):
    symbol = my_stock.symbol
    try:
        data = finnhub_client.company_basic_financials(symbol, metric='all')
        profile = finnhub_client.company_profile2(symbol=symbol)
        price = finnhub_client.quote(symbol=symbol)["c"]

    # This means we have reached our minute limit for Finnhub API calls and must wait 60 seconds
    except finnhub.FinnhubAPIException:
        print("sleeping")
        time.sleep(60)
        data = finnhub_client.company_basic_financials(symbol, metric='all')
        profile = finnhub_client.company_profile2(symbol=symbol)
        price = finnhub_client.quote(symbol=symbol)["c"]

    # Take only the metrics we are screening for
    my_stock.metrics = pick_metrics(data, translations)
    my_stock.industry = profile["finnhubIndustry"]
    my_stock.market_cap = round(profile["marketCapitalization"], 2)
    my_stock.price = price

    return my_stock

# Find matches for a given set of criteria and stock objects
def find_matches(stocks, criteria):
    matches = []
    print("finding matches")
    for stock in stocks:
        if match_conditions(criteria, stock.metrics):
            matches.append(stock)
    return matches

# Take only the metrics we are screening for
# This is a helper function for add_metrics
def pick_metrics(data_dict: dict, translations: dict):
    metric_dict = dict()
    for criterion in translations.keys():
        try:
            metric_dict[criterion] = data_dict['metric'][translations[criterion]]
        except KeyError:
            pass
    return metric_dict

# Check if a stock matches the given criteria
# This is a helper function for find_matches
def match_conditions(criteria: dict, metrics: dict):
    for m in criteria.keys():
        if m not in metrics.keys():
            return False
        v = metrics[m]
        (c, t) = criteria[m]
        if type(v) in (int, float):
            if c == '>':
                if not v > t:
                    return False
            elif c == '<':
                if not v < t:
                    return False
    return True
