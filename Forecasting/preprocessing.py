import pandas as pd

def preprocessing(df):
    price = df["Close"][9000:]

    price = price.groupby(pd.PeriodIndex(price.index, freq="M")).mean()

    y = price.copy()
    X = make_lags(y, 24).dropna()
    y = make_multistep_target(y, 12).dropna()

    return X[:-11], y[24:]

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

