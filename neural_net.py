from sklearn.neural_network import MLPRegressor
import datetime
import pickle

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
