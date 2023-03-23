import load
import preprocessing
from hybrid import hybrid
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

def train_hybrid(X1, X2, y, dp):
    model = hybrid()
    model.train(X1, X2, y, dp)

    filename = "model.sav"
    pickle.dump(model, open(filename, "wb"))

    return X1, X2, y


df = load.load()
X1, y, dp = preprocessing.preprocessing(df, 3)

X2 = preprocessing.make_lags(y, 15).dropna()

# train_hybrid(X1, X2, y, dp)
model = pickle.load(open("model.sav", "rb"))

d = ["1939-07-21", "2020-11-04"]
y_fit = model.predict(d, X2)

print("R^2 score:", r2_score(y[15:], y_fit))

ax = y.plot(color="black")
y_fit.plot(ax=ax, color="blue")

plt.show()
