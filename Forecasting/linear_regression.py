import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import datetime
# import pickle

class linearRegression:
    def __init__(self):
        self.lin_reg = LinearRegression()

    def train(self, X, y):
        now = datetime.datetime.now()

        self.lin_reg.fit(X, y)

        y_pred = pd.Series(self.lin_reg.predict(X), index=X.index)
        # y_fore = pd.Series(lin_reg.predict(X_fore), index=X_fore.index)

        ax = y.plot()
        y_pred.plot(ax=ax, color="blue")
        # y_fore.plot(ax=ax, color="red", linestyle="dashed")

        plt.show()
        print("Trained linear regression in", (datetime.datetime.now() - now).microseconds / 1000, "milliseconds")
        print("MSE of LR: ", mean_squared_error(y, y_pred))

        # filename = "lin_reg.sav"
        # pickle.dump(self.lin_reg, open(filename, "wb"))

    def predict(self, X):
        # filename = "lin_reg.sav"
        return pd.Series(self.lin_reg.predict(X), index=X.index)
