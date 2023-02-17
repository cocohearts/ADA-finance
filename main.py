import load
import preprocessing
import linear_regression
import neural_net

df = load.load()
X, y, _ = preprocessing.preprocessing(df, 4, 1000)
linear_regression.train(X, y)

y_resid = y - linear_regression.predict(X)
y_resid = y_resid.stack().squeeze()

