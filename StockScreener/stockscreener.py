import finnhub
import time
import pickle

# Values are terms from Finnhub API documentation - see pins in Discord
translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
        'PM5Y': 'netProfitMargin5Y', 'ROAE': 'roae5Y', 'DE': 'totalDebt/totalEquityAnnual',
        'CR': 'currentRatioAnnual', 'FCF': 'focfCagr5Y0', 'EPSG': 'epsGrowth5Y'}

names = {'PE': 'NormalizedPE', 'PB': 'Price/Book', 'RG5Y': '5YRevGrowth', 'PS': 'Price/Sales',
                'PM5Y': '5YProfit', 'ROAE': 'roae5Y', 'DE': 'Debt/Equity',
                'CR': 'Assets/Liabilities', 'FCF': "FreeCashFlow", 'EPSG': '5YEPSGrowth'}

finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")

industries = sorted(set([company.industry for company in pickle.load(open("StockScreener/companies.p", "rb"))]))
industry_values = list(range(len(industries)))

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
