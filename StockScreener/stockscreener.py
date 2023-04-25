import stockscreener_functions
import finnhub
import time
import pickle

# Feel free to add more metrics if you want
criteria = {'PE': ('<', 10), 'PB': ('<', 0.7), 'RG5Y': ('>', 10), 'PS': ('<', 1), 'PM5Y': ('>', 30),
             'ROAE': ('>', 10), 'DE': ('<', 50), 'CR': ('>', 1.5)}
# (For demo) criteria = {'PE': ('<', 10), 'PB': ('<', 0.7)}

# Values are terms from Finnhub API documentation - see pins in Discord
translations = {'PE': 'peNormalizedAnnual', 'PB': 'pbAnnual', 'RG5Y': 'revenueGrowth5Y', 'PS': 'psTTM',
                'PM5Y': 'netProfitMargin5Y', 'ROAE': 'roae5Y', 'DE': 'totalDebt/totalEquityAnnual',
                'CR': 'currentRatioAnnual'}

finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")

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
    match = []
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
            c.market_cap = round(profile["marketCapitalization"], 2)

            try:
                c.price = finnhub_client.quote(symbol=symbol)["c"]
            except finnhub.FinnhubAPIException:
                print("sleeping")
                time.sleep(60)
                c.price = finnhub_client.company_profile2(symbol=symbol)["c"]

            match.append(c)
    return match


# companies = pickle.load(open("companies.p", "rb"))
# matches = find_matches(companies, criteria)