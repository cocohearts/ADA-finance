import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
import datetime
# import pickle
import pandas as pd

class neural_net:
    def __init__(self):
        self.neural_net = MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=5000, learning_rate_init=0.01)
    def train(self, X_train, y_train):
        now = datetime.datetime.now()
        self.neural_net.fit(X_train, y_train)

        print("Trained neural net in", (datetime.datetime.now() - now).microseconds / 1000, "milliseconds")
        # filename = "neural_net.sav"
        # pickle.dump(neural_net, open(filename, "wb"))

    def predict(self, X):
        return self.neural_net.predict(X)

    def test(self, X_test, y_test):
        # filename = "neural_net.sav"
        # neural_net = pickle.load(open(filename, "rb"))
        print("Score of NN:", round(self.neural_net.score(X_test, y_test), 4), end="")

    def plot(self, X, y):
        # filename = "neural_net.sav"
        # neural_net = pickle.load(open(filename, "rb"))
        y_fit = pd.DataFrame(self.neural_net.predict(X), index=X.index, columns=y.columns)
        ax = y[y.columns[0]].plot(color="black")
        y_fit[y_fit.columns[0]].plot(ax=ax, color="blue")

        plt.show()
