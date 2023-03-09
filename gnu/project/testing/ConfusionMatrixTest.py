'''
Created on Oct 29, 2020

@author: nastasvi
'''
import unittest

from project.tagger.Tagger import Tagger
from project.tagger.data.ConfusionMatrix import ConfusionMatrix

from pathlib import Path

class ConfusionMatrixTest(unittest.TestCase):


    def setUp(self):
        self.filename = "H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\wsj_dev.treetags"
        #"../Data/wsj_dev.treetags"


    def testConfusionMatrix(self):
        data = None
        try:
            data = Tagger.readCoNLL(self.filename)
        except (RuntimeError): 
            print("Error reading data from file {}".format(self.filename))

        cm = ConfusionMatrix(data)

        #//cm.print()        
        cm.print_d(5)
        print("\n")

        self.assertEqual(3621, cm.numberErrors("NN", "NN"))
        self.assertEqual(11, cm.numberErrors("NN", "NP"))
        self.assertEqual(0, cm.numberErrors("NP", "NN"))
        self.assertEqual(0, cm.numberErrors("NP", "NNP"))
        self.assertEqual(2500, cm.numberErrors("NNP", "NP"))

        Tagger.extractInstances(data, "NN", "NP")



if __name__ == "__main__":
    unittest.main()
