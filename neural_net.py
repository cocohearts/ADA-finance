from sklearn.neural_network import MLPRegressor

def train(X, y):
    model = MLPRegressor()  # TODO Tune hyperparameters
    model.fit(X, y)
