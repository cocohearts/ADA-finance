from re import template
from flask import Flask, render_template, request
from StockScreener.stock import *
from StockScreener.stockscreener import *
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html.j2')

@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/screener')
def screener():
    return render_template('screener.html.j2',items = translations.keys(), translations = translations)

@app.route('/screener_results', methods = ['POST'])
def screener_results():
    criteria = {}
    for item in translations:
        item_value = request.values.get(item+"_val")
        item_value = float(item_value)
        item_dir = request.values.get(item+"_dir")
        criteria[item] = (item_dir,item_value)
    
    companies = pickle.load(open("companies.p", "rb"))
    print(companies[0].metrics)
    # companies = {}

    matches = find_matches(companies, criteria)
    print(len(matches))
    print(criteria)

    return render_template('screener_results.html.j2',items = translations.keys(), translations = translations, matches=matches)

@app.route('/forecast')
def forecast():
    dataframe = pd.read_csv(filepath_or_buffer="prediction.txt")
    prediction = {}

    return render_template('forecast.html.j2',prediction = dataframe)