import matplotlib
from statsmodels.tsa.deterministic import DeterministicProcess
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd


def preprocessing(df, order):
    price = df["Close"][9000:]

    """
    trend = price.rolling(
        window=14,
        center=True,
        min_periods=7
    ).mean()

    ax = price.plot()
    trend.plot(ax=ax, linewidth=3)
    matplotlib.pyplot.show()
    """

    y = price.copy()
    X = y.array
    first = y.index()[0]
    return X, y

def make_lags(ts, lags):
    return pd.concat(
        {
            f'y_lag_{i}': ts.shift(i)
            for i in range(1, lags + 1)
        },
        axis=1)

def make_multistep_target(ts, steps):
    return pd.concat(
        {f'y_step_{i + 1}': ts.shift(-i)
         for i in range(steps)},
        axis=1)

def array_to_series(arr, first):
    return pd.series(arr, )