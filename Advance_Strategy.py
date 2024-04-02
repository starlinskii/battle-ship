import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LogisticRegression

class LinReg(BaseEstimator, RegressorMixin):

    def __init__(self, batch_size=25, num_steps=350, lr=1e-2):
        self.batch_size = batch_size
        self.num_steps = num_steps

    def fit(self, X, Y):
        w = np.random.randn(X.shape[1])[:None]
        n_object = len(X)

        for i in range(self.num_steps):
            sample_indices = np.random.randint(n_objects, size=self.batch_size)
            w -= 2 * self.lr * X[sample_indices].T @ (X[sample_indices] @ w - Y[sample_indices]) / self.batch
        
        self.w = w
        return self
    
    def predict(self, X):
        return X @ self.w

dataset = datasets.load_iris()
print(dataset.DESCR)
featurs = dataset.data
target = dataset.target

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
for i, axis in enumerate(axes.flat):
    axis.hist(featurs[:, i])
    axis.set_xlabel(dataset.feature_names[i])
    axis.set_ylabel('numbers of objects')

n_features = 10
n_objects = 10
w_true = np.random.normal(size=(n_features))

X = np.random.uniform(-5, 5, (n_objects, n_features))
X *= (np.arange(n_features) * 2 + 1)[np.newaxis, :]
Y = X.dot(w_true) + np.random.normal(0, 1, n_objects)
w = np.random.uniform(-2, 2, n_features)
n = 10
learning_rate = 1e-2

#gradient boosting
for i in range(n):
    w -= 2 * learning_rate * X.T @ (X @ w - Y) / Y.size

batch = 10
#stochastic gradient boosting 
for i in range(n):
    koef = learning_rate / (i + 1)
    indeces = np.random.randint(n_objects, size=batch)
    w -= 2 * koef * X[indeces].T @ (X[indeces] @ w - Y[indeces]) / batch

def expected_value():
    def a():
        pass




