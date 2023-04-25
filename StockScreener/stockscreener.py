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

# This part is the part that takes five minutes to run
""" 
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
companies = [Stock(symbol=sp500["Symbol"][i], name=sp500["Security"][i]) for i in range(len(sp500))]
for i in range(len(companies)):
    if i % 10 == 0:
        print(f"Getting metrics for {i}th company")
    companies[i] = get_metrics(companies[i])
print("Done getting metrics") """

# TODO Alex Zhao store the data in companies array (type: Stock) somehow, right now it's being pickled into "companies.p"

# pickle.dump(companies, open("companies.p", "wb"))


companies = pickle.load(open("companies.p", "rb"))
matches = find_matches(companies, criteria)
for c in matches:
    print(c.symbol, c.name, c.metrics, c.industry, c.market_cap, c.price)
