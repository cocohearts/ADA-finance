from collections import defaultdict
import pandas as pd


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


def write_to_excel_and_save(location, stocks):
    data = defaultdict(list)
    for s in stocks:
        data['Ticker'].append(s.symbol)
        data['Name'].append(s.name)
        data['Current Price'].append(s.c_price)
        data['Industry'].append(s.industry)
        data['Market Cap'].append(s.market_cap)
    result_df = pd.DataFrame(data)
    result_df.to_csv(location)
