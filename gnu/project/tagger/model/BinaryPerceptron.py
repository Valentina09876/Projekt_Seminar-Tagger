"""

"""
import numpy as np

from project.tagger.data import Token
from project.tagger.data import Sentence
from project.tagger.model import BinaryWeights

import random

class BinaryPerceptron(object):
    """
    Classdoc

    This class uses BinaryWeights to crate BinaryPerceptrons

    """

    def __init__(self, dim):
        """
        Constructor

        Each BinaryPerceptron-Object has a dimension, its weights and a list of visited tokens
        """
        self.dim = dim
        self.weights = BinaryWeights.BinaryWeights(self.dim)
        self.visited_token = []

    def predict(self, token: Token) -> int:
        """
        Makes a classification decision for a token

        @param token: token, which is getting a classification
        """

        if token not in self.visited_token:
            token.predictedLabelIndex = 0
            self.visited_token.append(token)

            return 0

        elif self.weights.score(token.features) > 0:
            token.predictedLabelIndex = token.correctLabelIndex

            return token.correctLabelIndex

        else:
            return 0

    def train(self, training_data: list[Sentence], development_data: list[Sentence] = None, num_of_iterations: int = 1):
        """
        Train the binary-perceptron-model

        @param training_data: the data to train
        @param development_data: the data to develop
        @param num_of_iterations: the amount of iterations required to train teh data
        """

        for sentence in training_data:
            for token in sentence.tokens:
                self.visited_token.append(token)
                for iteration in range(num_of_iterations):
                    if self.predict(token) != token.correctLabelIndex:
                        self.weights.update(feature_vector=token.features,
                                            learning_rate=0.5)
                    else:
                        break
