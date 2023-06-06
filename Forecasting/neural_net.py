from preprocessing import make_lags
from keras.models import Sequential
from keras.layers import *
import datetime
import pandas as pd
import tensorflow as tf

class neural_net:
    def __init__(self, nn=None):
        # Create a new model object or reuse an existing one
        if nn is None:
            self.neural_net = Sequential()
        else:
            self.neural_net = nn

    def train(self, X_train, y_train, epochs):
        now = datetime.datetime.now()

        # Create the model
        self.neural_net.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        self.neural_net.add(Dropout(0.2))
        self.neural_net.add(LSTM(units=50, return_sequences=True))
        self.neural_net.add(Dropout(0.2))
        self.neural_net.add(LSTM(units=50))
        self.neural_net.add(Dense(1, activation="linear"))
        sgd = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.neural_net.compile(optimizer=sgd, loss='mean_squared_error')

        # Train the model
        self.neural_net.fit(X_train, y_train, epochs=epochs,
                            callbacks=tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10))
        print("Trained neural net in", (datetime.datetime.now() - now).seconds, "seconds")

    def predict(self, X):
        return self.neural_net.predict(X, verbose=0)

    def predict_future(self, y, f):
        # This expands the time series f steps into the future
        y_future = pd.concat([y, pd.Series({y.index.shift(j)[-1]: 0 for j in range(1, f + 1)})])
        # Loops through each step and populates the time series
        for i in range(1, f + 1):
            # Next datapoint to be predicted
            X_future = make_lags(y_future, 24).dropna().iloc[-f + i - 1]
            # Predicts the next datapoint and fills in the time series
            y_future[y.index.shift(i)[-1]] = self.predict(pd.DataFrame(X_future).T)[0][0]

        # Returns only the future part of the series
        return y_future.iloc[-f:]

    def save(self, path):
        # Saves the inner Keras object so the model can be reconstructed later
        self.neural_net.save(path)
