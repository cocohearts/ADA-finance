from re import template
from flask import Flask, render_template, request
from StockScreener import stock
from StockScreener.stock import *
from StockScreener.stockscreener import *
import pickle
import pandas as pd
import itertools
import json

from load_metrics import load_metrics
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# scheduling load_metrics
scheduler = BackgroundScheduler()
scheduler.add_job(load_metrics, 'interval', days=1)
scheduler.start()

@app.route('/')
def main():
    return render_template('main.html.j2')

@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/screener')
def screener():
    items = translations.keys()
    tips = []
    with open('static/criteriatips.txt') as info:
        for line in info:
            tips.append(line)
    return render_template('screener.html.j2', items=items, names=names,
                           industries=industries, industry_values=industry_values, tips=tips, loops=zip(items, tips))

@app.route('/search_results', methods=['GET'])
def search_results():
    companies = pickle.load(open("StockScreener/companies.p", "rb"))
    matches = companies
    c = request.values.get("search")
    print(c)
    for i in matches:
        print(i.name)
        print(i.symbol)
    if c != "":
        i = 0
        while i < len(matches):
            company = matches[i]
            if company.name != c and company.symbol != c.upper():
                matches.remove(company)
            else:
                i += 1
    if len(matches) == 0 or len(matches) > 1:
        tips = []
        with open('static/criteriatips.txt') as info:
            for line in info:
                tips.append(line)
        return render_template('screener.html.j2', error="none", items=translations.keys(),
                               names=names, industries=industries, industry_values=industry_values,
                               tips=tips, loops=zip(translations.keys(), tips))
    return render_template('screener_results.html.j2', items=translations.keys(), names=names, matches=matches, criteria={})

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

    tips = []
    with open('static/criteriatips.txt') as info:
        for line in info:
            tips.append(line)

    if industry_val != "0":
        try:
            industry = industries[int(industry_val)]
        except IndexError:
            return render_template('screener.html.j2', error="industry", items=translations.keys(), names=names,
                                   industries=industries, industry_values=industry_values, tips=tips,
                                   loops=zip(translations.keys(), tips))
        i = 0
        while i < len(matches):
            company = matches[i]
            if company.industry != industry:
                matches.remove(company)
            else:
                i += 1

    if len(matches) == 0:
        return render_template('screener.html.j2', error="none", items=translations.keys(), names=names,
                               industries=industries, industry_values=industry_values, tips=tips,
                               loops=zip(translations.keys(), tips))

    # For some reason Jinja kept breaking when I tried to index a tuple inside a dictionary
    for key in criteria.keys():
        criteria[key] = criteria[key][0] + " " + str(criteria[key][1])
    
    with open("predictions/growth.json","r") as file:
        ticker_growth_dict = json.load(file)
    print(ticker_growth_dict)

    return render_template('screener_results.html.j2', items=translations.keys(), names=names, matches=matches,
                           criteria=criteria, industry=industry, ticker_growth_dict=ticker_growth_dict)

@app.route('/forecast',methods=['GET'])
def forecast():
    top = list(pd.read_csv("predictions/top.txt")['0'])
    with open("predictions/growth.json","r") as file:
        ticker_growth_dict = json.load(file)

    return render_template('forecast.html.j2',top=top,ticker_growth_dict=ticker_growth_dict)

@app.route('/forecast_results',methods=['GET','POST'])
def forecast_results():
    ticker = request.values.get("ticker")
    if ticker == None:
        ticker = request.args.get("ticker")
    if ticker:
        graph_image_path = f"static/predictiongraphs/{ticker}_predictiongraph.png"
    else:
        graph_image_path = None
    top = list(pd.read_csv("predictions/top.txt")['0'])

    return render_template('forecast_results.html.j2',graphpath=graph_image_path,top=top)