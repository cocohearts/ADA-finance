import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import datetime
import numpy as np
# import pickle

class exponentialRegression:
    def __init__(self, X, y):
        now = datetime.datetime.now()
        self.exp_reg = np.polyfit(X, np.log(y), 1)
        self.a = np.e ** self.exp_reg[1]
        self.b = np.e ** self.exp_reg[0]

        y_fit = pd.Series(self.a * self.b ** X, index=X.index)

        ax = y.plot()
        y_fit.plot(ax=ax, color="blue")

        plt.show()

        print("Trained exponential regression in", (datetime.datetime.now() - now).microseconds / 1000, "milliseconds")
        print("MSE of ER: ", mean_squared_error(y, y_fit))

    def predict(self, X):
        return pd.Series(self.a * self.b ** X, index=X.index)
