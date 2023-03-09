'''
Created on Oct 29, 2020
HAllo Test
@author: nastasvi
'''

#import io

from project.tagger.data import Sentence
from project.tagger.data import Token
from project.tagger.data.StringMapper import StringMapper
from datetime import datetime
from project.tagger.model.FeatureExtractors import FeatureExtractors
from project.tagger.model.Perceptron import Perceptron
from project.tagger.model.Evaluation import Evaluation
# from project.tagger.data.ConfusionMatrix import  ConfusionMatrix

# do not import from data with a dot: import .data - this throws an error
class Tagger(object):
    '''
    Class to create a Tagger

    with a method to read CoNLL-files, and return them as a List of sentences

    with a method to extract Instances of how often a specific gold Label
    occurs with a specific prediction Label

    '''
    @staticmethod
    def readCoNLL(filename:str) -> list[Sentence]:
        """
        Method to read a CoNLL file
        Converts all Sentences in The file to a Sentence-Object consisting of a List of Token-Objects

        @param: filename, path for the file to read
        """

        stringMapper = StringMapper()

        with open(filename, "r", encoding="utf-8") as file:
            sentences = []
            current_sentence = []
            prev_token = Token.Token('BOS', label='BOS', correctLabelIndex=0)

            for line in file:
                column = line.split("\t")

                if column[0] == '\n':
                    sentences.append(Sentence.Sentence(current_sentence))
                    prev_token.next = Token.Token('EOS', label='EOS')
                    prev_token = Token.Token('BOS', label='BOS', correctLabelIndex=0)
                    current_sentence = []

                else:
                    tokens = Token.Token(word=column[1],
                                         label=column[4],
                                         prediction=column[5],
                                         previous=prev_token,
                                         correctLabelIndex=stringMapper.lookup(column[4]),
                                         predictedLabelIndex=stringMapper.lookup(column[5]))
                    current_sentence.append(tokens)

                    # the current token is the next's previous token
                    if len(current_sentence) > 1:
                        prev_token.next = current_sentence[-1]  # current token
                    prev_token = current_sentence[-1]     # previous token
        return sentences



    def extractInstances(data, goldLabel, predLabel):
        """
        Method to extract Instances of how often a specific gold Label
        occurs with a specific prediction Label
        """
        def print_instances(word, gold_standard, prediction):
            """
            Method to print all Instances as requiered in the exercise

            @param: word, represents the token
            @param: gold_standard, represents the gold standard Label
            @param: prediction: represents the prediction Label
            """
            print('\t', word, '\t', gold_standard, '\t', prediction)

        for sentence in data:
            for index in range(sentence.length()):

                if sentence.get(index).label == goldLabel and sentence.get(index).prediction == predLabel:
                    if index-3 >= 0:
                        print_instances(sentence.get(index-3).word, sentence.get(index-3).label, sentence.get(index-3).prediction)
                    if index-2 >= 0:
                        print_instances(sentence.get(index-2).word, sentence.get(index-2).label, sentence.get(index-2).prediction)
                    if index-1 >= 0:
                        print_instances(sentence.get(index-1).word, sentence.get(index-1).label, sentence.get(index-1).prediction)

                    print_instances('*' + sentence.get(index).word + '*', sentence.get(index).label, sentence.get(index).prediction)

                    if index+1 <= sentence.length()-1:
                        print_instances(sentence.get(index+1).word, sentence.get(index+1).label, sentence.get(index+1).prediction)
                    if index+2 <= sentence.length()-1:
                        print_instances(sentence.get(index+2).word, sentence.get(index+2).label, sentence.get(index+2).prediction)
                    if index+3 <= sentence.length()-1:
                        print_instances(sentence.get(index+3).word, sentence.get(index+3).label, sentence.get(index+3).prediction)

                    print('*********')



    @staticmethod
    def out_last_line(filename: str):
        """
        Just a Test-Method to find out where the file ends
        """
        with open(filename, "r", encoding="utf-8") as file:
            list_of_lines = []

            for line in file:  # "split" at \n
                list_of_lines.append(line)

            print(list_of_lines[-1])

    @staticmethod
    def pipeline():
        """
        Tagger pipeline
        """

        # read in Data - Training
        start_time = datetime.now()
        print("Load training data...")
        train_data = Tagger.readCoNLL("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\wsj_train.conll09")
        train_data = train_data[:1000]
        print("done.")

        # "new" Data - Prediction -development
        print("Load development data...")
        dev_data = Tagger.readCoNLL("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\wsj_dev.conll09")
        print("done.")

        # "test" Data - Testing
        print("Load test data...")
        test_data = Tagger.readCoNLL("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\wsj_test.conll09")
        print("done.")

        # train data hart codieren
        print("Create tag-set over train data...")
        tags = dict()
        for sentence in train_data:
            for token in sentence.tokens:
                tags.update({token.correctLabelIndex: token.label})
        print("done. \n")

        # Extract features for all Data
        print("Extract features...")
        featureExtractor = FeatureExtractors()
        print("train_data \n")
        featureExtractor.extractAllFeatures(train_data)
        print("dev_data \n")
        featureExtractor.extractAllFeatures(dev_data)
        print("test_data \n")
        featureExtractor.extractAllFeatures(test_data)

        print("train features... ")
        train_features = featureExtractor.stringMapper.feature_dict.keys()
        print("done.\n")

        print("Number of features: ", len(train_features))

        # Extract Class Index for all Data

        print("Extract Class Index for all Data")
        train_class_indexes = set()
        for sentence in train_data:
            for token in sentence.tokens:
                train_class_indexes.add(token.correctLabelIndex)
        print("Number of classes: ", len(train_class_indexes))

        # Perceptron
        # train data hart codieren

        print("Initialize perceptron...")
        perceptron = Perceptron(len(train_class_indexes), len(train_features), debug=True)
        print("done.")

        print("Train perceptron...", "\n")
        start_training = datetime.now()
        perceptron.train(train_data, dev_data, 2)  # evtl mehr durchläufe, aber dauert dann auch länger!
        print("\n", "done in", datetime.now() - start_training, "\n")


        # inspect trained developement data
        """
        print("cases of wrong predictions")
        print("with dev_data")

        pred_incorrect = {}
        for sentence in dev_data:
            for token in sentence.tokens:
                if token.prediction != token.label:
                    pred_incorrect[token.label] = token.prediction
        print(pred_incorrect)


        print("ConfusionMatrix for dev_data: ")
        cm = ConfusionMatrix(dev_data)
        cm.print_d(7)
        cm.print_d(10)
        """


        #Tagger.extractInstances(dev_data, "NN", "NNP") #736
        #Tagger.extractInstances(dev_data, "JJ", "NNP") #336
        #Tagger.extractInstances(dev_data, "NNS", "NNP") #290
        #Tagger.extractInstances(dev_data, "NNP", "NN")  #189
        #Tagger.extractInstances(dev_data, "JJ", "NN")  #158

        #keinere Anzahl:

        #Tagger.extractInstances(dev_data, "NNP", "JJ") #54
        #Tagger.extractInstances(dev_data, "NN", "JJ")  #43
        #Tagger.extractInstances(dev_data, "IN", "NNP") #24
        #Tagger.extractInstances(dev_data, "NN", "NNS") #16
        #Tagger.extractInstances(dev_data, "NNP", "DT") #16
        #Tagger.extractInstances(dev_data, "NNP", "NNS") #15
        #Tagger.extractInstances(dev_data, "NN", "IN") #6
        #Tagger.extractInstances(dev_data, "DT", "NN") #6
        #Tagger.extractInstances(dev_data, "NNP", "IN") #5
        #Tagger.extractInstances(dev_data, "JJ", "IN") #5


        # Vorhersagen auf neuen Daten machen
        print("Predictions on test-data...")
        start_prediction = datetime.now()

        for sentence in test_data:
            for token in sentence.tokens:
                perceptron.predict(token)
                token.prediction = tags[token.predictedLabelIndex]
        print("done in", datetime.now() - start_prediction, "\n")
        print('#' * 75)

        # print("Train  Accuracy:", Evaluation.accuracy(train_data), "\n")
        print("Test Accuracy:", Evaluation.accuracy(test_data), "\n")
        print("Runtime:", datetime.now() - start_time)






if __name__ == '__main__':
   #path = "H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\tiger-2.2.train.conll09"
   #tagger = Tagger.readCoNLL(path)
   Tagger.pipeline()











