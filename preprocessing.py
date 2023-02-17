import load
import matplotlib
from statsmodels.tsa.deterministic import DeterministicProcess


def preprocessing(df, order, fore):
    price = df["Close"]

    trend = price.rolling(
        window=14,
        center=True,
        min_periods=7
    ).mean()

    # ax = price.plot()
    # trend.plot(ax=ax, linewidth=3)
    # matplotlib.pyplot.show()

    y = trend.copy()
    dp = DeterministicProcess(
        index=y.index,
        order=order
    )

    X = dp.in_sample()
    X_fore = dp.out_of_sample(fore)

    return X, y, X_fore

