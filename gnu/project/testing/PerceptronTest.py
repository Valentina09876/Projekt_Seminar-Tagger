'''
Created on Oct 30, 2020

@author: nastasvi
'''
import unittest

from project.tagger.model.Weights import Weights
from project.tagger.model.Perceptron import Perceptron

from project.tagger.data.Sentence import Sentence
from project.tagger.data.Token import Token

class PerceptronTest(unittest.TestCase):


    def testWeights(self):
        weights = Weights(3, 5)

        #// first, try to update the weights with a feature vector
        featureVector1 = [1,2,3]
        weights.update(1, 0, featureVector1, 0.5)
        score1 = weights.score(1, featureVector1)
        self.assertAlmostEqual(-2, score1, 2, "Score should be 4 * -0.5 = -2")

        #// now try to score another feature vector
        featureVector2 = [1,2,99]
        score2 = weights.score(0, featureVector2)
        self.assertAlmostEqual(1.5, score2, 2, "Score should be 3 * 0.5 = 1.5")


    def testPerceptron(self):
        perceptron = Perceptron(3, 10)
        trainSentenceList = self.generateTrainSentences()

        perceptron.train(trainSentenceList, 3)

        i = 0
        for w_i in perceptron.weights.weights:
            print("Weights for class {}:  {}".format(i, w_i))
            i += 1

        #// make a prediction for the first token
        token1 = trainSentenceList[0].get(0)
        prediction1 = perceptron.predict(token1)
        expected1 = token1.correctLabelIndex
        self.assertEqual(expected1, prediction1, "Prediction for the first token should be 1")

        #// make a prediction for the last token
        token4 = trainSentenceList[0].get(3)
        prediction4 = perceptron.predict(token4)
        expected4 = token4.correctLabelIndex
        self.assertEqual(expected4, prediction4, "Prediction for the fourth token should be 0")


        #// make a prediction for an unseen token
        testToken = self.generateTestToken()
        predictionTest = perceptron.predict(testToken)
        self.assertEqual(testToken.correctLabelIndex, predictionTest, "Prediction for the unseen token should be 2")
        self.assertEqual(testToken.predictedLabelIndex, predictionTest, "Prediction should be saved in token!")



    def generateTrainSentences(self):
        testSentenceList = []
        testSentence = Sentence()
        testSentenceList.append(testSentence)


        token1 = Token()
        token1.features = [1,2,3]
        token1.correctLabelIndex = 1
        testSentence.add(token1)

        token2 = Token()
        token2.features = [2,3]
        token2.correctLabelIndex = 1
        testSentence.add(token2)

        token3 = Token()
        token3.features = [4,5,6]
        token3.correctLabelIndex = 0
        testSentence.add(token3)

        token4 = Token()
        token4.features = [5,6]
        token4.correctLabelIndex = 0
        testSentence.add(token4)

        token5 = Token()
        token5.features = [7,8,9]
        token5.correctLabelIndex = 2
        testSentence.add(token5)

        token6 = Token()
        token6.features = [9,8]
        token6.correctLabelIndex = 2
        testSentence.add(token6)

        return testSentenceList

    
    def generateTestToken(self):
        testToken = Token()
        testToken.correctLabelIndex = 2
        testToken.features = [1,5,7,8,9]
        return testToken



if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
