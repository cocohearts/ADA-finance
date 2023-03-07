from sklearn.model_selection import train_test_split
import load
import preprocessing
import linear_regression
import neural_net

df = load.load()
X1, y, _ = preprocessing.preprocessing(df, 4, 1000)
linear_regression.train(X1, y)

y_resid = y - linear_regression.predict(X1)
y_resid = y_resid.squeeze()

X2 = preprocessing.make_lags(y_resid, 14).dropna()
y2 = preprocessing.make_multistep_target(y_resid, 7).dropna()

y2, X2 = y2.align(X2, join='inner', axis=0)

X_train, X_test, y_train, y_test = train_test_split(X2, y2, test_size=0.25, shuffle=False)
neural_net.train(X_train, y_train)
neural_net.test(X_test, y_test)

# neural_net.plot(X2, y2)
