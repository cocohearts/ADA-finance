from sklearn.model_selection import train_test_split
import load
import preprocessing
import linear_regression
import neural_net
from hybrid import hybrid

df = load.load()
X, y, X_fore_1 = preprocessing.preprocessing(df, 4, 14)

model = hybrid()
model.train(X, y)

