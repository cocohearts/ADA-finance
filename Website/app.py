from re import template
from flask import Flask, render_template
from flask_crontab import Crontab
from Vertex.predict import *

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
    return render_template('screener.html.j2')

@app.route('/forecast')
def forecast():
    return render_template('forecast.html.j2')

@crontab.job(minute="0", hour="0")
def my_scheduled_job():
    exec(open("../Vertex/pipeline_setup.py").read())
    call_model()