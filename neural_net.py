import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
import datetime
import pickle
import pandas as pd

def train(X_train, y_train):
    now = datetime.datetime.now()
    neural_net = MLPRegressor()  # TODO Tune hyperparameters
    neural_net.fit(X_train, y_train)

    print("Trained neural net in", (datetime.datetime.now() - now).microseconds / 1000, "milliseconds")
    filename = "neural_net.sav"
    pickle.dump(neural_net, open(filename, "wb"))

def test(X_test, y_test):
    filename = "neural_net.sav"
    neural_net = pickle.load(open(filename, "rb"))
    print("Score of NN:", neural_net.score(X_test, y_test))

def plot(X, y):
    filename = "neural_net.sav"
    neural_net = pickle.load(open(filename, "rb"))
    y_fit = pd.DataFrame(neural_net.predict(X), index=X.index, columns=y.columns)
    ax = y[y.columns[0]].plot(color="black")
    y_fit[y_fit.columns[0]].plot(ax=ax, color="blue")

    plt.show()
