from sklearn.model_selection import train_test_split
import preprocessing
import linear_regression
import neural_net

class hybrid:
    def __init__(self):
        self.lr = None
        self.nn = None
        self.dp = None

    def train(self, X1, X2, y, dp):
        self.dp = dp

        self.lr = linear_regression.linearRegression()
        self.lr.train(X1, y)

        y_resid = y - self.lr.predict(X1)
        y_resid = y_resid.squeeze()

        y2 = preprocessing.make_multistep_target(y_resid, 10).dropna()

        y2, X2 = y2.align(X2, join='inner', axis=0)

        X_train, X_test, y_train, y_test = train_test_split(X2, y2, test_size=0.15, shuffle=False)

        self.nn = neural_net.neural_net()
        self.nn.train(X_train, y_train)
        self.nn.test(X_train, y_train)
        print(" on train set")
        self.nn.test(X_test, y_test)
        print(" on test set")

        self.nn.plot(X2, y2)

    # Function predict
    # Parameters
    # d (str): date range to generate prediction for
    # (First date, last date)
    # (If one day, pass in just one date)
    # X2 (Dataframe): Dataframe with index as dates in date range
    # Columns: y_lag_1, y_lag_2, ... y_lag_15
    # X2[date][y_lag_3] = Price 3 days before the date
    # X2[date][y_lag_1] = Price 1 day before the date
    # Output (Series): Prediction of price for next 5 days
    def predict(self, d, X2):
        X1 = self.dp.range(d[0], d[-1])
        y_pred = self.lr.predict(X1)
        y_pred_2 = self.nn.predict(X2)
        y_pred_boosted = y_pred_2[:, 0] + y_pred

        return y_pred_boosted
