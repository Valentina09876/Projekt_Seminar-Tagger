'''
Created on Oct 29, 2020
HAllo Test
@author: nastasvi
'''

import pandas as pd
from nltk.metrics import ConfusionMatrix as cm
from project.tagger.data.Sentence import Sentence
# from project.tagger import Tagger


class ConfusionMatrix(object):
    '''
    Class to create a Confusion-Matrix

    with methods to create and return a confusion Matrix, specified by a List of Sentences

    '''

    def __init__(self, sentences: list[Sentence]):
        '''
        Constructor for The Class Confusion Matrix

        every instance of a Confusion Matrix, has a list of Sentences and a Confusion-Matrix
        '''

        self.sentences = sentences
        self.confusionmatrix = self.__create_confusion_m()

    def __create_confusion_m(self):
        """
        with the function ConfusionMatrix from the nltk.metrics package

        we create the ConfusionMatrix, based on gold- and prediction_label of each token

        """

        gold_standard = []
        prediction = []
        # first build the structure of the confusion matrix

        for sentence in self.sentences:
            for token in sentence.tokens:
                gold_standard.append(token.label)
                prediction.append(token.prediction)
        return cm(gold_standard, prediction, sort_by_count=True)



    def numberErrors(self, goldLabel:str, predLabel:str) -> int:
        """
        returns the amount of tags with a specific gold_label and a specific pred_label
        """
        return self.confusionmatrix[goldLabel, predLabel]

    def print_d(self, max_dim: int):
        """
        prints the Confusion-Matrix, with a specific limit of arg: max_dim

        @param: max_dim, specified limit for ConfusionMatrix size.
                row and colums of ConfusionMatrix do not exceed max_dim
        """

        gold_standard = self.confusionmatrix.__dict__['_indices']
        prediction = self.confusionmatrix.__dict__['_values']

        data_frame = pd.DataFrame(self.confusionmatrix.__dict__['_confusion'], index=gold_standard, columns=prediction)

        if max_dim:
            data_frame = data_frame[data_frame.index[:max_dim]]   # limit the amount of columns first
            data_frame = data_frame.loc[data_frame.columns.values.tolist(), :]  # then limit the amount of rows

            # loc the information for a list of values in the rows, and just print them

        print(data_frame)




#if __name__ == '__main__':
    # = "H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\wsj_dev.treetags"
    #tagger = Tagger.Tagger.readCoNLL(path)
    #print(ConfusionMatrix(tagger).print_d(5))











