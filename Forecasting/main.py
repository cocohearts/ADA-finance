import load
import preprocessing
from neural_net import neural_net
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import pandas as pd
import keras
import glob

df = load.load("SPX.csv")

X, y = preprocessing.preprocessing(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, shuffle=False)

start_train = y_train[0]
start_test = y_test[0]

X_train = preprocessing.to_percent(X_train)
X_test = preprocessing.to_percent(X_test)
y_train = preprocessing.to_percent(y_train)
y_test = preprocessing.to_percent(y_test)

X_train_exp = X_train.copy()
X_test_exp = X_test.copy()
y_train_exp = y_train.copy()
y_test_exp = y_test.copy()

for path in list(glob.iglob('../data/*.csv')):
    df = load.load(path)
    X_temp, y_temp = preprocessing.preprocessing(df)

    if len(X_temp) < 10:
        continue

    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_temp, y_temp, test_size=0.15, shuffle=False)

    X_train_temp = preprocessing.to_percent(X_train_temp)
    X_test_temp = preprocessing.to_percent(X_test_temp)
    y_train_temp = preprocessing.to_percent(y_train_temp)
    y_test_temp = preprocessing.to_percent(y_test_temp)

    X_train_exp = pd.concat([X_train_exp, X_train_temp])
    X_test_exp = pd.concat([X_test_exp, X_test_temp])
    y_train_exp = pd.concat([y_train_exp, y_train_temp])
    y_test_exp = pd.concat([y_test_exp, y_test_temp])

print("Preprocessed %d datapoints" % (len(y_train_exp) + len(y_test_exp)))

# model = neural_net()
# model.train(X_train_exp, y_train_exp, 50)

# model.save("model.sav")
model = neural_net(keras.models.load_model("model.sav"))

fit = model.predict(X_train)
y_fit = pd.Series(fit[:, 0].astype(float), index=X_train.index)

pred = model.predict(X_test)
y_pred = pd.Series(pred[:, 0].astype(float), index=X_test.index)


# Predict future values
f = 60
last = y.iloc[-1]
y_future = pd.concat([y, pd.Series({y.index.shift(j)[-1]: 0 for j in range(1, f+1)})])

for i in range(1, f+1):
    X_future = preprocessing.make_lags(y_future, 24).dropna().iloc[-1-i]
    y_future[y.index.shift(i)[-1]] = model.predict(pd.DataFrame(X_future).T)[0][0]

y_future = y_future.iloc[-f:]

print("R^2 score on train set:", r2_score(y_train, y_fit))
print("R^2 score on test set:", r2_score(y_test, y_pred))

y = pd.Series(y, index=X.index)
y_fit = preprocessing.to_values(start_train, pd.Series(y_fit, index=X_train.index))
y_pred = preprocessing.to_values(start_test, pd.Series(y_pred, index=X_test.index))
y_future = preprocessing.to_values(last, y_future)

ax = y.plot(color="black")
y_fit.plot(ax=ax, color="blue")
y_pred.plot(ax=ax, color="red")

plt.show()

ax = y.plot(color="black")
y_future.plot(ax=ax, color="red")

plt.show()