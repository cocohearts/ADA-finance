from re import template
from flask import Flask, render_template
app = Flask(__name__)

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