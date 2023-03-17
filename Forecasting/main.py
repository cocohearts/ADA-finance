import load
import preprocessing
from hybrid import hybrid
import pickle
import matplotlib.pyplot as plt

def train_hybrid(X1, X2, y):
    model = hybrid()
    model.train(X1, X2, y)

    filename = "model.sav"
    pickle.dump(model, open(filename, "wb"))

    return X1, X2, y


df = load.load()
X1, y, X_fore_1 = preprocessing.preprocessing(df, 3, 14)
X2 = preprocessing.make_lags(y, 14).dropna()

train_hybrid(X1, X2, y)
model = pickle.load(open("model.sav", "rb"))

y_fit = model.predict(X1, X2)

ax = y.plot(color="black")
y_fit.plot(ax=ax, color="blue")

plt.show()
