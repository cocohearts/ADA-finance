import load
import preprocessing
from neural_net import neural_net
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd

df = load.load()
X, y = preprocessing.preprocessing(df)

model = neural_net()
model.train(X, y)

joblib.dump(model, open("model.sav", "wb"))
# model = joblib.load(open("model.sav", "rb"))

fit = model.predict(X)
idx = pd.to_datetime(fit[:, 1][:, 1])
idx.freq = 'B'
y_fit = pd.Series(fit[:, 0][:, 0].astype(float), index=idx)

print("R^2 score:", r2_score(y[15:], y_fit))

ax = y[15:].plot(color="black")
y_fit.plot(ax=ax, color="blue")

plt.show()
