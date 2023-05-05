import load
import preprocessing
from neural_net import neural_net
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

df = load.load()
X, y = preprocessing.preprocessing(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

model = neural_net()
model.train(X_train, y_train)

# model.save("model.sav")
# model = keras.models.load_model('model.sav')

fit = model.predict(X_train)
y_fit = pd.Series(fit[:, 0].astype(float), index=X_train.index)

pred = model.predict(X_test)
y_pred = pd.Series(pred[:, 0].astype(float), index=X_test.index)

print("R^2 score on train set:", r2_score(y_train, y_fit))
print("R^2 score on test set:", r2_score(y_test, y_pred))

ax = y.plot(color="black")
y_fit.plot(ax=ax, color="blue")
y_pred.plot(ax=ax, color="red")

plt.show()
