'''
Created on Oct 29, 2020

@author: nastasvi
'''

from project.tagger.data import Sentence
from project.tagger.data import Token

class Evaluation(object):
    '''
    classdocs
    '''

    @staticmethod
    def accuracy(data: list[Sentence]):
        pred_correct = 0
        pred_total = 0
        for sentence in data:
            for token in sentence.tokens:
                pred_total += 1
                pred_correct += token.prediction == token.label

        return pred_correct / pred_total
