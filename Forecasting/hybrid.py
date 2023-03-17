from sklearn.model_selection import train_test_split
import preprocessing
import linear_regression
import neural_net

class hybrid:
    def __init__(self):
        self.lr = None
        self.nn = None

    def train(self, X1, X2, y):
        self.lr = linear_regression.linearRegression()
        self.lr.train(X1, y)

        y_resid = y - self.lr.predict(X1)
        y_resid = y_resid.squeeze()

        y2 = preprocessing.make_multistep_target(y_resid, 7).dropna()

        y2, X2 = y2.align(X2, join='inner', axis=0)

        X_train, X_test, y_train, y_test = train_test_split(X2, y2, test_size=0.15, shuffle=False)

        self.nn = neural_net.neural_net()
        self.nn.train(X_train, y_train)
        self.nn.test(X_train, y_train)
        print(" on train set")
        self.nn.test(X_test, y_test)
        print(" on test set")

        self.nn.plot(X2, y2)

    def predict(self, X1, X2):
        y_pred = self.lr.predict(X1)
        y_pred_2 = self.nn.predict(X2)
        y_pred_boosted = y_pred_2[:,0] + y_pred[14:]

        return y_pred_boosted
