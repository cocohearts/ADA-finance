import load
import preprocessing
from hybrid import hybrid
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd

def train_hybrid(X1, X2, y, fore, dp):
    hyb = hybrid()
    hyb.train(X1, X2, y, fore, dp)

    filename = "model.sav"
    joblib.dump(hyb, open(filename, "wb"))

    return X1, X2, y


df = load.load()
X1, y, dp = preprocessing.preprocessing(df, 5)

X2 = preprocessing.make_lags(y, 15).dropna()

train_hybrid(X1, X2, y, 5, dp)
model = joblib.load(open("model.sav", "rb"))

# Current prediction
p = np.array([3936.97, 4002.87, 3951.57, 3916.64, 3960.28, 3891.93, 3919.29, 3855.76, 3861.59, 3918.32, 3992.01, 3986.37, 4048.82, 4045.64, 3981.35])
print(model.predict(["2023-03-23"], p.reshape(1, -1)))

d = [str(X2.index[0]).split(" ")[0], "2020-11-04"]
fit = model.predict(d, X2)
idx = pd.to_datetime(fit[:, 1][:, 1])
idx.freq = 'B'
y_fit = pd.Series(fit[:, 0][:, 0].astype(float), index=idx)

print("R^2 score:", r2_score(y[15:], y_fit))

ax = y[15:].plot(color="black")
y_fit.plot(ax=ax, color="blue")

plt.show()
