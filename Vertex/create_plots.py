from os import listdir
import matplotlib.pyplot as plt
import pandas as pd

import os
import glob

files = glob.glob('static/predictiongraphs/*')
for f in files:
    os.remove(f)

output_names = listdir('predictions/')
loaded_count = 0

for prediction_filename in output_names:
    if prediction_filename[-3:] != "csv":
        continue
    df = pd.read_csv(f'predictions/{prediction_filename}')
    
    ticker = prediction_filename[:-15]
    dates = [f'{date[5:7]}/{date[2:4]}' for date in list(df['Unnamed: 0'])]
    values = list(df['close'])

    vals = pd.Series(data=values,index=dates)
    old_vals = pd.Series(data=values[:-60],index=dates[:-60])
    new_vals = pd.Series(data=values[-25:],index=dates[-25:])

    ax = vals.plot(style="g.-")
    old_vals.plot(color="black",style=".-")

    n=19
    residue = len(dates)-1-n*int(len(dates)/n)
    tick_indices = [residue+int(len(dates)/n)*r for r in range(n+1)]
    tick_months = [dates[tick_index] for tick_index in tick_indices]
    ax.set_xticks(tick_indices)
    ax.set_xticklabels(tick_months,rotation = 45)

    ax.set_ylabel("Price ($)")
    ax.set_xlabel("Month")
    ax.set_ylim(ymin=0)
    ax.set_title(f"Past and Predicted Price Values for {ticker}")
    plt.grid()

    prediction_graphname = f"static/predictiongraphs/{ticker}_predictiongraph.png"
    plt.savefig(prediction_graphname)

    plt.close()