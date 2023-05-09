import finnhub
import time

# Feel free to add more metrics if you want
# criteria = {'PE': ('<', 10), 'PB': ('<', 0.7), 'RG5Y': ('>', 10), 'PS': ('<', 1), 'PM5Y': ('>', 30),
#              'ROAE': ('>', 10), 'DE': ('<', 50), 'CR': ('>', 1.5)}

# Values are terms from Finnhub API documentation - see pins in Discord
# translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
#                 'PM5Y': 'netProfitMargin5Y', 'ROAE': 'roae5Y', 'DE': 'totalDebt/totalEquityAnnual',
#                 'CR': 'currentRatioAnnual'}

translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
                'DE': 'totalDebt/totalEquityAnnual','CR': 'currentRatio'}

names = {'PE': 'Annual Norm PE', 'PB': 'Price/Book Annual', 'RG5Y': '5Y Revenue Growth', 'PS': 'Price/Sales Trailing 12M',
                'DE': 'Annual Debt/Equity','CR': 'Assets/Liabilities Ratio'}

finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")

def add_metrics(my_stock):
    symbol = my_stock.symbol
    
    try:
        data = finnhub_client.company_basic_financials(symbol, metric='all')
        profile = finnhub_client.company_profile2(symbol=symbol)
        price = finnhub_client.quote(symbol=symbol)["c"]
    except:
        print("sleeping")
        time.sleep(60)
        data = finnhub_client.company_basic_financials(symbol, metric='all')
        profile = finnhub_client.company_profile2(symbol=symbol)
        price = finnhub_client.quote(symbol=symbol)["c"]

    my_stock.metrics = pick_metrics(data, translations)
    my_stock.industry = profile["finnhubIndustry"]
    my_stock.market_cap = round(profile["marketCapitalization"], 2)
    my_stock.price = price

    return my_stock

def find_matches(stocks, criteria):
    matches = []
    print("finding matches")
    for stock in stocks:
        if match_conditions(criteria, stock.metrics):
            matches.append(stock)
    return matches

def pick_metrics(data_dict: dict, translations: dict):
    metric_dict = dict()
    for criterion in translations.keys():
        try:
            metric_dict[criterion] = data_dict['metric'][translations[criterion]]
        except KeyError:
            pass
    return metric_dict

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