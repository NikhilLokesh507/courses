import math


def distance(p1, p2):
    assert len(p1) == len(p2)
    return math.sqrt(sum((p1[i]-p2[i])**2 for i in range(len(p1))))


class KNNClassifier:
    """
    KNN classifier
    """

    def __init__(self, X, y, k):
        """
        Initialize a KNN-classifier from given dataset

        args:
            X: list of data points
            y: list of class of given data points
            k: k neighbors are used to classify a data point
        """
        self.X, self.y = X, y
        self.k = k

    def classify(self, point):
        """
        classify a point using KNN principle
        """
        dists = [(i,distance(x, point)) for i, x in enumerate(self.X)]
        sorted_dists = sorted(dists, key=lambda x: x[1])

        k_nbs = sorted_dists[:self.k]
        votes = {}
        for i, _ in k_nbs:
            if self.y[i] not in votes:
                votes[self.y[i]] = 1
            else:
                votes[self.y[i]] += 1
        return max(votes, key=votes.get)

    def batch_classify(self, points):
        return [self.classify(point) for point in points]

