import load
import matplotlib
from statsmodels.tsa.deterministic import DeterministicProcess
import pandas as pd


def preprocessing(df, order, fore):
    price = df["Close"][2000:]

    trend = price.rolling(
        window=14,
        center=True,
        min_periods=7
    ).mean()

    # ax = price.plot()
    # trend.plot(ax=ax, linewidth=3)
    # matplotlib.pyplot.show()

    y = price.copy()
    dp = DeterministicProcess(
        index=trend.index,
        order=order
    )

    X = dp.in_sample()
    X_fore = dp.out_of_sample(fore)
    return X, y, X_fore

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
