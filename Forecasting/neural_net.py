import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import numpy as np
from keras.models import Sequential
from keras.layers import *
import datetime
import pandas as pd
import tensorflow as tf

class neural_net:
    def __init__(self, nn=None):
        # self.neural_net = MLPRegressor(hidden_layer_sizes=(100, 200, 100), max_iter=5000, learning_rate_init=0.001,
        #                              tol=0.0001, alpha=0.00001)

        if nn is None:
            self.neural_net = Sequential()
        else:
            self.neural_net = nn

    def train(self, X_train, y_train, epochs):
        now = datetime.datetime.now()
        self.neural_net.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        self.neural_net.add(Dropout(0.2))
        self.neural_net.add(LSTM(units=50, return_sequences=True))
        self.neural_net.add(Dropout(0.2))
        self.neural_net.add(LSTM(units=50))
        self.neural_net.add(Dense(1, activation="linear"))
        sgd = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.neural_net.compile(optimizer=sgd, loss='mean_squared_error')
        self.neural_net.fit(X_train, y_train, epochs=epochs,
                            callbacks=tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10))
        print("Trained neural net in", (datetime.datetime.now() - now).seconds, "seconds")

    def predict(self, X):
        return self.neural_net.predict(X)

    def test(self, X_test, y_test):
        y_pred = np.array(self.predict(X_test))
        print("MSE of NN:", mean_squared_error(y_pred, y_test), " ")

    def plot(self, X, y):
        y_fit = pd.DataFrame(self.neural_net.predict(X), index=X.index, columns=y.columns)
        ax = y[y.columns[0]].plot(color="black")
        y_fit[y_fit.columns[0]].plot(ax=ax, color="blue")

        plt.show()

    def save(self, path):
        self.neural_net.save(path)
