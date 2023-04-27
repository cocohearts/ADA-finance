import finnhub
import time

# Feel free to add more metrics if you want
criteria = {'PE': ('<', 10), 'PB': ('<', 0.7), 'RG5Y': ('>', 10), 'PS': ('<', 1), 'PM5Y': ('>', 30),
             'ROAE': ('>', 10), 'DE': ('<', 50), 'CR': ('>', 1.5)}
# (For demo) criteria = {'PE': ('<', 10), 'PB': ('<', 0.7)}

# Values are terms from Finnhub API documentation - see pins in Discord
# translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
#                 'PM5Y': 'netProfitMargin5Y', 'ROAE': 'roae5Y', 'DE': 'totalDebt/totalEquityAnnual',
#                 'CR': 'currentRatioAnnual'}

translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
                'DE': 'Debt/EquityAnnual','CR': 'currentRatio'}

finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")

def get_metrics(c):
    symbol = c.symbol
    try:
        data = finnhub_client.company_basic_financials(symbol, metric='all')
    except finnhub.FinnhubAPIException:
        print("sleeping")
        time.sleep(60)
        data = finnhub_client.company_basic_financials(symbol, metric='all')

    c.metrics = insert_metrics(data, criteria, translations)
    return c

def find_matches(stocks, criteria):
    match = []
    print("finding matches")
    for c in stocks:
        symbol = c.symbol
        if match_conditions(criteria, c.metrics):
            try:
                profile = finnhub_client.company_profile2(symbol=symbol)
            except finnhub.FinnhubAPIException:
                print("sleeping")
                time.sleep(60)
                profile = finnhub_client.company_profile2(symbol=symbol)

            c.industry = profile["finnhubIndustry"]
            c.market_cap = round(profile["marketCapitalization"], 2)

            try:
                c.price = finnhub_client.quote(symbol=symbol)["c"]
            except finnhub.FinnhubAPIException:
                print("sleeping")
                time.sleep(60)
                c.price = finnhub_client.company_profile2(symbol=symbol)["c"]

            match.append(c)
    return match


def insert_metrics(data_dict: dict, criteria: dict, translations: dict):
    stock_dict = dict()
    for c in criteria.keys():
        try:
            stock_dict[c] = data_dict['metric'][translations[c]]
        except KeyError:
            pass
    return stock_dict

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