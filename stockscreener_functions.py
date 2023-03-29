import time
from collections import defaultdict
from pathlib import Path
import datetime as dt
import finnhub
import pandas as pd


# Function from NeuralNine Stock Screener Tutorial
def fixed_delay(call, **kwargs):
    start = time.perf_counter() + 1
    try:
        print(call)
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


def match_conditions(criteria: dict[str: tuple], metrics: dict[str: int]):
    count = 0
    for m, v in metrics.items():
        (c, t) = criteria[m]
        if type(v) in (int, float):
            if c == '>':
                if not v > t:
                    return False
            elif c == '<':
                if not v < t:
                    return False
            elif c == '>=':
                if not v >= t:
                    return False
            elif c == '<=':
                if not v <= t:
                    return False
    return True

def create_file_path(file_name: str, folder_path: Path):
    destination = folder_path / f"{file_name}.csv"
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
    result_df.to_csv(location)
