import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocessing(df):
    price = df["Close"][9000:]
    price = price.groupby(pd.PeriodIndex(price.index, freq="M")).mean()

    values = price.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_price = scaler.fit_transform(pd.DataFrame(values))

    y = pd.Series(scaled_price[:, 0], index=price.index)
    X = make_lags(y, 24).dropna()

    return X, y[24:], scaler

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

