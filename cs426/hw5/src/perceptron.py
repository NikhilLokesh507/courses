import numpy as np


class PerceptronClassifier:
    """
    Perceptron Algorithm for classification
    """
    def __init__(self, X, y, lr=0.01):
        """
        Train a perceptron classifier from given dataset

        args:
            X: list of data points
            y: list of class of given data points, must be value of 1, -1
            lr: learning rate
        """
        dim = len(X[0])
        self.X, self.y = np.array(X), np.array(y)
        self.lr = lr

        # model intialization
        self.W = np.zeros(dim)
        self.b = 0

        self.fit()

    def fit(self):
        """
        train the model to fit the dataset
        """
        converge = False
        while not converge:
            converge = True
            for xi, yi in zip(self.X, self.y):
                yhat = self.classify(xi)
                if yhat != yi:
                    converge = False
                    # update model
                    self.W += self.lr * yi * xi
                    self.b += self.lr * yi * 1

    def classify(self, point):
        pv = (self.W * point).sum() + self.b
        return 1 if pv >= 0 else -1

    def batch_classify(self, points):
        return [self.classify(point) for point in points]

