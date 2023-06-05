from re import template
from flask import Flask, render_template, request
from StockScreener import stock
from StockScreener.stock import *
from StockScreener.stockscreener import *
import pickle
import pandas as pd
import itertools

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html.j2')

@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/screener')
def screener():
    items=translations.keys()
    tips = []
    with open('static/criteriatips.txt') as info:
        for line in info:
            tips.append(line)
    print (tips)
    return render_template('screener.html.j2', items=translations.keys(), names=names,
                           industries=industries, industry_values=industry_values, tips=tips, loops=zip(items,tips))

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
    if len(matches)==0:
        none=True
        return render_template('screener.html.j2', n=none, items=translations.keys(), names=names, industries=industries, industry_values=industry_values)
    return render_template('screener_results.html.j2', items=translations.keys(), names=names, matches=matches)

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

    if industry_val != "0":
        industry = industries[int(industry_val)]
        i = 0
        while i < len(matches):
            company = matches[i]
            if company.industry != industry:
                matches.remove(company)
            else:
                i += 1

    # For some reason Jinja kept breaking when I tried to index a tuple inside a dictionary
    for key in criteria.keys():
        criteria[key] = criteria[key][0] + " " + str(criteria[key][1])

    return render_template('screener_results.html.j2', items=translations.keys(), names=names, matches=matches,
                           criteria=criteria, industry=industry)

@app.route('/forecast',methods=['GET'])
def forecast():
    top10 = list(pd.read_csv("predictions/top10.txt")['0'])

    return render_template('forecast.html.j2',top10=top10)

@app.route('/forecast_results',methods=['GET','POST'])
def forecast_results():
    ticker = request.values.get("ticker")
    if ticker:
        graph_image_path = f"static/predictiongraphs/{ticker}_predictiongraph.png"
    else:
        graph_image_path = None
    top10 = list(pd.read_csv("predictions/top10.txt")['0'])

    return render_template('forecast_results.html.j2',graphpath=graph_image_path,top10=top10)