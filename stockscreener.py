from queue import SimpleQueue, Empty
import stock as Stock
import finnhub
import time 
import pandas as pd
from collections import defaultdict
from pathlib import Path
import datetime as dt


finnhub_client = finnhub.Client(api_key="cdq10f2ad3i5u3ridjs0cdq10f2ad3i5u3ridjsg")

criteria = {'PE': ('<', 10), 'PB': ('<=', 0.7), 'RG5Y': ('>=', 10), 'PS': ('<', 1)}

# Function from Neural9 Stock Screener Tutorial
def fixed_delay(call, **kwargs):
    start = time.perf_counter() + 1
    try:
        ret = call(**kwargs)
    except finnhub.FinnhubAPIException:
        time.sleep(60)
        ret = call(**kwargs)
    diff = start - time.perf_counter()
    if diff > 0:
        time.sleep(diff)
    return ret


def insert_metrics(data_dict: dict):
    stock_dict = dict()
    try:
        stock_dict['PE'] = data_dict['metric']['peNormalizedAnnual']
        stock_dict['PB'] = data_dict['metric']['pbAnnual']
        stock_dict['RG5Y'] = data_dict['metric']['revenueGrowth5Y']
        stock_dict['PS'] = data_dict['metric']['psTTM']
    except KeyError:
        pass
    return stock_dict


def match_conditions(metrics: dict[str: int]):
    count = 0
    for m, v in metrics.items():
        c, t = criteria[m]
        if type(v) in (int, float):
            if c == '>':
                if v > t:
                    count += 1
            elif c == '<':
                if v < t:
                    count += 1
            elif c == '>=':
                if v >= t:
                    count += 1
            elif c == '<=':
                if v <= t:
                    count += 1
    return count == len(criteria) - 1

def create_file_path(file_name: str, folder_path: Path):
    c_time = dt.datetime.now()
    destination = folder_path / f"{file_name}.xlsx"
    return destination


def write_to_excel_and_save(location, u_stocks_data):
    excel_data = defaultdict(list)
    current = dt.datetime.now()
    today = f"{current.month}/{current.day}/{current.year}"
    for stocks in u_stocks_data:
        excel_data['Ticker'].append(stocks.symbol)
        excel_data['Name'].append(stocks.name)
        excel_data['Current Price'].append(stocks.c_price)
        excel_data['Exchange'].append(stocks.exchange)
        excel_data['Industry'].append(stocks.industry)
        excel_data["Company's website"].append(stocks.web_url)
        excel_data["Date"].append(today)
    result_df = pd.DataFrame(excel_data)
    result_df.to_excel(location)
