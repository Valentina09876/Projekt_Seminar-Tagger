"""

"""
import random
from project.tagger.data import Sentence
from project.tagger.data import Token
from project.tagger.model.Weights import Weights
from project.tagger.model.Evaluation import Evaluation


class Perceptron(object):
    """
    Classdoc
    """

    def __init__(self, num_classes: int, num_features: int, debug: bool = False):
        """
        Constructor
        """
        self.num_classes = num_classes
        self.num_features = num_features
        self.weights = Weights(self.num_classes, self.num_features)
        self.debug = debug

    def predict(self, token: Token) -> int:

        scores = [self.weights.score(class_index, token.features) for class_index in range(self.num_classes)]
        token.predictedLabelIndex = scores.index(max(scores))
        return token.predictedLabelIndex

    def train(self, training_data: list[Sentence], development_data: list[Sentence] = None,
              number_of_iterations: int = 1):

        # create tag-set
        tags = dict()
        for sentence in training_data:
            for token in sentence.tokens:
                tags.update({token.correctLabelIndex: token.label})

        if development_data:
            development_tokens = []
            for sentence in development_data:
                for token in sentence.tokens:
                    development_tokens.append(token)

        for _ in range(number_of_iterations):   #train iteration
            for sentence in training_data:
                random.shuffle(sentence.tokens)

                for token in sentence.tokens:
                    prediction = self.predict(token)
                    self.weights.update(prediction, token.correctLabelIndex, token.features, 0.5)

                    # solve some issues
                    if token.predictedLabelIndex > 0:
                        token.prediction = tags[token.predictedLabelIndex]


            if development_data:
                for token in development_tokens:
                    self.predict(token)
                    token.prediction = tags[token.predictedLabelIndex]


            # Blatt5 Aufgabe 3
            if self.debug:
                print("#" * 75)
                print("Iteration: ", _ + 1)
                print("train accuracy: ", round(Evaluation.accuracy(training_data), 3))

            if development_data and self.debug:
                print("development accuracy: ", round(Evaluation.accuracy(development_data), 3))



