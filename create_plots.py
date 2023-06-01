from os import listdir
import matplotlib.pyplot as plt
import pandas as pd

prediction_names = listdir('predictions/')
loaded_count = 0
for prediction_filename in prediction_names:
    ticker = prediction_filename[:-9]
    try:
        df = pd.read_csv(f'predictions/{prediction_filename}')
    except:
        continue

    ticker = prediction_filename[:-15]
    df = pd.read_csv(f'predictions/{prediction_filename}')
    dates = [f'{date[5:7]}/{date[2:4]}' for date in list(df['Unnamed: 0'])]
    values = list(df['close'])
    # plt.plot(dates,prev_values,'b--',dates,new_values,'r--')

    fig,ax=plt.subplots()
    # ax=fig.add_axes([1,2,1,1])
    ax.plot(values,'--')
    ax.set_xlabel("Month")
    ax.set_ylabel("Price ($)")

    # plt.plot(dates,values,'--')
    n=17
    residue = len(dates)-1-n*int(len(dates)/n)
    tick_indices = [residue+int(len(dates)/n)*r for r in range(n+1)]
    tick_months = [dates[tick_index] for tick_index in tick_indices]
    ax.set_xticks(tick_indices)
    ax.set_xticklabels(tick_months,rotation = 45)

    ax.set_title(f"Past and Predicted Price Values for {ticker}")
    plt.grid()
    prediction_graphname = f"predictiongraphs/{ticker}_predictiongraph.png"
    fig.savefig(prediction_graphname)

    plt.close(fig)