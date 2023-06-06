from os import listdir
import matplotlib.pyplot as plt
import pandas as pd

import os
import glob

# clear existing prediction graphs
files = glob.glob('static/predictiongraphs/*')
for f in files:
    os.remove(f)

# get prediction csv names
output_names = listdir('predictions/')

for prediction_filename in output_names:
    # check in case it is a growth log
    if prediction_filename[-3:] != "csv":
        continue
    df = pd.read_csv(f'predictions/{prediction_filename}')
    
    ticker = prediction_filename[:-15]
    # dates and values are lists
    dates = [f'{date[5:7]}/{date[2:4]}' for date in list(df['Unnamed: 0'])]
    values = list(df['close'])

    vals = pd.Series(data=values,index=dates)
    old_vals = pd.Series(data=values[:-60],index=dates[:-60])

    # old_vals will cover up vals
    ax = vals.plot(style="g.-")
    old_vals.plot(color="black",style=".-")

    # add tick marks
    n=19
    residue = len(dates)-1-n*int(len(dates)/n)
    tick_indices = [residue+int(len(dates)/n)*r for r in range(n+1)]
    tick_months = [dates[tick_index] for tick_index in tick_indices]
    ax.set_xticks(tick_indices)
    ax.set_xticklabels(tick_months,rotation = 45)
    
    plt.grid()
    ax.set_ylim(ymin=0)

    ax.set_ylabel("Price ($)")
    ax.set_xlabel("Month")
    ax.set_title(f"Past and Predicted Price Values for {ticker}")

    prediction_graphname = f"static/predictiongraphs/{ticker}_predictiongraph.png"
    plt.savefig(prediction_graphname)

    plt.close()