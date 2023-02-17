import preprocessing
import matplotlib
from sklearn.linear_model import LinearRegression
import pandas as pd

X, y, X_fore = preprocessing.preprocessing(3, 1000)

lin_reg = LinearRegression()
lin_reg.fit(X, y)

y_pred = pd.Series(lin_reg.predict(X), index=X.index)
y_fore = pd.Series(lin_reg.predict(X_fore), index=X_fore.index)

ax = y.plot()
y_pred.plot(ax=ax, color="blue")
y_fore.plot(ax=ax, color="red", linestyle="dashed")

matplotlib.pyplot.show()