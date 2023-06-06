import pandas as pd

# Load dataset from path and preprocess it
def preprocessing(path):
    df = pd.read_csv(path)
    df = df.set_index(pd.to_datetime(df["date"]))
    df = df.fillna(method="ffill")
    price = df["close"]
    # Take monthly datapoints
    price = price.groupby(pd.PeriodIndex(price.index, freq="M")).mean()

    y = price
    X = make_lags(y, 24).dropna()

    return X, y[24:]

# Return a dataframe that is 'ts', but lagged once, twice, etc. up to 'lags' times
# i.e. The first row of the returned dataframe will have the *last* 'lags' values of 'ts'
def make_lags(ts, lags):
    return pd.concat(
        {
            f'y_lag_{i}': ts.shift(i)
            for i in range(1, lags + 1)
        },
        axis=1)

# Same thing as 'make_lags()', but shifts the data forward instead of backward
# i.e. The first row of the returned dataframe will have the *next* 'steps' values of 'ts'
def make_multistep_target(ts, steps):
    return pd.concat(
        {f'y_step_{i + 1}': ts.shift(-i)
         for i in range(steps)},
        axis=1)

# Converts a dataframe of values to a dataframe of percent change from the previous value
def to_percent(df):
    return df.pct_change().dropna()

# Converts a dataframe of percent change from the previous value to a dataframe of values
# i.e. reverses 'to_percent()'
def to_values(start, y_pred):
    return pd.concat([pd.Series({y_pred.index.shift(-1)[0]: start}),
                      y_pred.add(1, fill_value=0).cumprod()*start])