import pandas as pd
import preprocessing

df = preprocessing.load()
trend = df.rolling(
    window=14,
    center=True,
    min_periods=7
).mean()

ax = df.plot()
ax = trend.plot(ax=ax, linewidth=3)

y = trend.copy()
dp = Determini