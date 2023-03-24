import load
import preprocessing
from hybrid import hybrid
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd

def train_hybrid(X1, X2, y, fore, dp):
    model = hybrid()
    model.train(X1, X2, y, fore, dp)

    filename = "model.sav"
    joblib.dump(model, open(filename, "wb"))

    return X1, X2, y


df = load.load()
X1, y, dp = preprocessing.preprocessing(df, 3)

X2 = preprocessing.make_lags(y, 15).dropna()

# train_hybrid(X1, X2, y, 5, dp)
model = joblib.load(open("model.sav", "rb"))

# Current prediction
p = np.array([3936.97, 4002.87, 3951.57, 3916.64, 3960.28, 3891.93, 3919.29, 3855.76, 3861.59, 3918.32, 3992.01, 3986.37, 4048.82, 4045.64, 3981.35])
print(model.predict(["2023-03-23"], p.reshape(1, -1)))

d = ["1939-07-21", "2020-11-04"]
y_fit = model.predict(d, X2)
y_fit = pd.Series(y_fit[:, 0][:, 0].astype(float), index=y_fit[:, 1][:, 1])

print("R^2 score:", r2_score(y[15:], y_fit))

ax = y.plot(color="black")
# CURRENTLY BROKEN
# y_fit.plot(ax=ax, color="blue")

plt.show()
