import matplotlib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import datetime
import pickle


def train(X, y):
    now = datetime.datetime.now()

    lin_reg = LinearRegression()
    lin_reg.fit(X, y)

    y_pred = pd.Series(lin_reg.predict(X), index=X.index)
    # y_fore = pd.Series(lin_reg.predict(X_fore), index=X_fore.index)

    # ax = y.plot()
    # y_pred.plot(ax=ax, color="blue")
    # y_fore.plot(ax=ax, color="red", linestyle="dashed")

    # matplotlib.pyplot.show()
    print("Trained linear regression in", (datetime.datetime.now() - now).microseconds / 1000, "milliseconds")
    print("MSE of LR: ", mean_squared_error(y, y_pred))

    filename = "lin_reg.sav"
    pickle.dump(lin_reg, open(filename, "wb"))


def predict(X):
    filename = "lin_reg.sav"
    lin_reg = pickle.load(open(filename, "rb"))
    return pd.Series(lin_reg.predict(X), index=X.index)
