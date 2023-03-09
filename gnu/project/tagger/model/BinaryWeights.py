

import numpy as np


class BinaryWeights(object):  #object should be an Array list with float values
    """
    administrates the weights of the model
    """

    def __init__(self, dim: int):
        """
        Constructor

        Each BinaryWeights-Object has a dimension and its weights
        @param: dim, dimension
        """
        self.dim = dim
        self.weights = np.array([0] * (self.dim+1))

    def score(self, feature_vector: list[int]):
        """
        Returns a Tokens feature-vector score

        calculates dot-product from: weight_vector and feature_vector
        @param: feature_vector, list of features

        """

        return self.weights.dot(self.__to_binary_vector(feature_vector))

    def update(self, feature_vector: list[int], learning_rate: float):
        """
        Update the weights for the given feature-vector
        add learning rate to weight_vector

        @param: feature_vector, list of features
        @param: learning_rate, to update weight_vector
        """
        expected = self.score(feature_vector)

        if expected > 0:
            prediction = 1
        else:
            prediction = 0

        self.weights = self.weights + learning_rate
        if expected != prediction:
            self.weights = self.weights * (expected - prediction) * self.__to_bnary_vector(feature_vector)

    def __to_binary_vector(self, feature_vector: list[int]) -> np.ndarray:
        """
        Converts a list of serialized features into a binary vector

        @param: feature_vector, list of features
        @return: binary vector

        """
        features = np.array([1] + [0] * self.dim)

        for index in feature_vector:
            if index <= self.dim + 1:
                features[index] = 1

        return features


