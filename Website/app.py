from re import template
from flask import Flask, render_template, request
from flask_crontab import Crontab
from Vertex.predict import *
from StockScreener.load_metrics import *

app = Flask(__name__)
crontab = Crontab(app)

@app.route('/')
def main():
    return render_template('main.html.j2')

@app.route('/about')
def about():
    return render_template('about.html.j2')

@app.route('/screener')
def screener():
    return render_template('screener.html.j2',items = translations.keys(), translations = translations)

@app.route('/screener_results')
def screener_results():
    criteria = {}
    for item in translations:
        item_value = request.values.get(item+"_val")
        item_dir = request.values.get(item+"_dir")
        criteria[item] = (item_dir,item_value)
    
    companies = pickle.load(open("../StockScreener/companies.p", "rb"))

    matches = find_matches(companies, criteria)

    return render_template('screener_results.html.j2',items = translations.keys(), translations = translations, matches=matches)

@app.route('/forecast')
def forecast():
    return render_template('forecast.html.j2')

@crontab.job(minute="0", hour="0")
def my_scheduled_job():
    exec(open("../Vertex/pipeline_setup.py").read())
    # for prediction
    call_model()
    # for stockscreener
    load_metrics()