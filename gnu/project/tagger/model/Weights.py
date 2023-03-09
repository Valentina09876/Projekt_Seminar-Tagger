import numpy as np


class Weights(object):
    """
    Classdocs

    This class expands the Perceprton to a multiclass Perceptron
    """

    def __init__(self, num_classes: int, num_features: int):
        """
        Constructor

        Each MulticlassPerceptron has:

        @param num_features: number of features
        @param num_classes: number of classes

        and weights of each of this amount of classes and features
        """
        self.num_classes = num_classes
        self.num_features = num_features
        self.weights = np.zeros((num_classes, num_features + 1))

    def score(self, class_ID: int, feature_vector: list[int]) -> float:
        """
        Retrurns a Tokens feature-vector score
        """
        return self.weights[class_ID].dot(self.__to_binary_vector(feature_vector))

    def update(self, prediction: int, correctLabelIndex: int, features: list[int], learning_rate: float):
        if correctLabelIndex < self.weights.shape[0] and prediction < self.weights.shape[0]:
            binary_vector = self.__to_binary_vector(features)
            self.weights[prediction] = self.weights[prediction] - learning_rate * binary_vector
            self.weights[correctLabelIndex] = self.weights[correctLabelIndex] + learning_rate * binary_vector



    def __to_binary_vector(self, vector: list[int])-> np.ndarray:
        """
        Converts a vector to a binary-vector

        """
        vector_len = self.num_features +1
        binary_vector = np.zeros(vector_len)
        binary_vector[0] = 1
        np.put(binary_vector, vector, 1, mode='clip')

        return binary_vector