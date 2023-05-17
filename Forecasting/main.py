import load
import preprocessing
from neural_net import neural_net
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import keras
import glob

## Load, preprocess, and split data

df = load.load("SPX.csv")

X, y = preprocessing.preprocessing(df)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, shuffle=False)

start_train = y_train[0]
start_test = y_test[0]

X = preprocessing.to_percent(X)
y = preprocessing.to_percent(y)
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

    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_temp, y_temp, test_size=0.15,
                                                                            shuffle=False)

    X_train_temp = preprocessing.to_percent(X_train_temp)
    X_test_temp = preprocessing.to_percent(X_test_temp)
    y_train_temp = preprocessing.to_percent(y_train_temp)
    y_test_temp = preprocessing.to_percent(y_test_temp)

    X_train_exp = pd.concat([X_train_exp, X_train_temp])
    X_test_exp = pd.concat([X_test_exp, X_test_temp])
    y_train_exp = pd.concat([y_train_exp, y_train_temp])
    y_test_exp = pd.concat([y_test_exp, y_test_temp])

print("Preprocessed %d datapoints" % (len(y_train_exp) + len(y_test_exp)))


## Train model

# model = neural_net()
# model.train(X_train_exp, y_train_exp, 200)

# model.save("model.sav")

model = neural_net(keras.models.load_model("model.sav"))


## Evaluate model

fit = model.predict(X_train)
y_fit = pd.Series(fit[:, 0].astype(float), index=X_train.index)

pred = model.predict(X_test)
y_pred = pd.Series(pred[:, 0].astype(float), index=X_test.index)

print("MSE on train set:", mean_squared_error(y_train, y_fit))
print("MSE on test set:", mean_squared_error(y_test, y_pred))


## Predict future values

ticker = "TRIP"
f = 60

df = load.load("../data/" + ticker + "_data.csv")
_, y_other = preprocessing.preprocessing(df)
assert len(y_other) > 24, "Not enough data for prediction"
first = y_other[0]
last = y_other[-1]
y_other = preprocessing.to_percent(y_other)
y_future = model.predict_future(y_other, f)


## Plot results

y = preprocessing.to_values(start_train, pd.Series(y, index=X.index))
y_fit = preprocessing.to_values(start_train, pd.Series(y_fit, index=X_train.index))
y_pred = preprocessing.to_values(start_test, pd.Series(y_pred, index=X_test.index))
y_other = preprocessing.to_values(first, y_other)
y_future = preprocessing.to_values(last, y_future)

ax = y.plot(color="black")
y_fit.plot(ax=ax, color="blue")
y_pred.plot(ax=ax, color="red")
plt.show()

ax = y_other.plot(color="black")
y_future.plot(ax=ax, color="red")
plt.show()
