import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocessing(df):
    price = df["close"]
    price = price.groupby(pd.PeriodIndex(price.index, freq="M")).mean()

    y = price
    X = make_lags(y, 24).dropna()

    return X, y[24:]

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


def to_percent(df):
    return df.pct_change().dropna()

def to_values(start, y_pred):
    return pd.concat([pd.Series({y_pred.index.shift(-1)[0]: start}),
                      y_pred.add(1, fill_value=0).cumprod()*start])