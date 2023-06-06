from flask import Flask, render_template, request
from StockScreener import stock
from StockScreener.stock import *
from StockScreener.stockscreener import *
import pickle
import pandas as pd
import json

from load_metrics import load_metrics
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt

app = Flask(__name__)

# Scheduling load_metrics
scheduler = BackgroundScheduler()
start_time = dt.datetime.now() + dt.timedelta(minutes=2)
scheduler.add_job(load_metrics, 'interval', minutes=1440,next_run_time=start_time)
scheduler.start()

@app.route('/')
def main():
    return render_template('main.html.j2')

# For the screener landing page
@app.route('/screener')
def screener():
    items = translations.keys()
    tips = []
    with open('static/criteriatips.txt') as info:
        for line in info:
            tips.append(line)
    return render_template('screener.html.j2', items=items, names=names,
                           industries=industries, industry_values=industry_values, tips=tips, loops=zip(items, tips))

# For the search bar on the screener page
@app.route('/search_results', methods=['GET'])
def search_results():
    companies = pickle.load(open("StockScreener/companies.p", "rb"))
    matches = companies
    c = request.values.get("ticker")
    if c != "":
        i = 0
        while i < len(matches):
            company = matches[i]
            if company.name != c and company.symbol != c.upper():
                matches.remove(company)
            else:
                i += 1
    # Certain nonsense inputs will cause the screener to preserve all 500 companies as matches, so I added this check
    if len(matches) == 0 or len(matches) > 1:
        tips = []
        with open('static/criteriatips.txt') as info:
            for line in info:
                tips.append(line)
        return render_template('screener.html.j2', error="none", items=translations.keys(),
                               names=names, industries=industries, industry_values=industry_values,
                               tips=tips, loops=zip(translations.keys(), tips))

    return render_template('screener_results.html.j2', items=translations.keys(), names=names, matches=matches, criteria={})

# For the other screener functions
@app.route('/screener_results', methods=['POST'])
def screener_results():
    criteria = {}
    for item in translations:
        try:
            item_value = request.values.get(item+"_val")
            item_value = float(item_value)
            item_dir = request.values.get(item+"_dir")
            criteria[item] = (item_dir, item_value)
        except ValueError:
            pass

    companies = pickle.load(open("StockScreener/companies.p", "rb"))
    matches = find_matches(companies, criteria)

    industry_val = request.values.get("industry_val")
    industry = None

    # Just in case there is an error, and we have to go back to the previous page
    tips = []
    with open('static/criteriatips.txt') as info:
        for line in info:
            tips.append(line)

    # 0 is the default blank value for the industry dropdown, so we ignore it
    if industry_val != "0":
        try:
            industry = industries[int(industry_val)]

        # Prevents the user from entering a value that is not in the dropdown by inspecting element
        except IndexError:
            return render_template('screener.html.j2', error="industry", items=translations.keys(), names=names,
                                   industries=industries, industry_values=industry_values, tips=tips,
                                   loops=zip(translations.keys(), tips))

        # Prune matches to only the ones with matching industry
        i = 0
        while i < len(matches):
            company = matches[i]
            if company.industry != industry:
                matches.remove(company)
            else:
                i += 1

    # If there are no matches, go back to previous page
    if len(matches) == 0:
        return render_template('screener.html.j2', error="none", items=translations.keys(), names=names,
                               industries=industries, industry_values=industry_values, tips=tips,
                               loops=zip(translations.keys(), tips))

    # For some reason Jinja kept breaking when I tried to index a tuple inside a dictionary
    # So I had to parse the tuples into strings first
    for key in criteria.keys():
        criteria[key] = criteria[key][0] + " " + str(criteria[key][1])

    return render_template('screener_results.html.j2', items=translations.keys(), names=names, matches=matches,
                           criteria=criteria, industry=industry)

# For forecasting landing page
@app.route('/forecast', methods=['GET'])
def forecast():
    top = list(pd.read_csv("predictions/top.txt")['0'])
    with open("predictions/growth.json", "r") as file:
        ticker_growth_dict = json.load(file)

    return render_template('forecast.html.j2', top=top, ticker_growth_dict=ticker_growth_dict)

# For forecasting pages of individual companies
@app.route('/forecast_results', methods=['GET', 'POST'])
def forecast_results():
    ticker = request.values.get("ticker")
    if ticker is None:
        ticker = request.args.get("ticker")
    if ticker:
        graph_image_path = f"static/predictiongraphs/{ticker}_predictiongraph.png"
    else:
        graph_image_path = None
    top = list(pd.read_csv("predictions/top.txt")['0'])

    return render_template('forecast_results.html.j2', graphpath=graph_image_path, top=top)
