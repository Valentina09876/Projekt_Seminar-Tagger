'''
Created on Oct 29, 2020

@author: nastasvi
'''
import unittest

from project.tagger.Tagger import *
from project.tagger.model.Evaluation import Evaluation

class EvaluationTest(unittest.TestCase):


    def setUp(self):

        self.filename = "H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\wsj_dev.treetags"


    def testAccuracy(self):
        #// check that the treetagger WSJ tags have the expected accuracy
        wsjFile = Tagger.readCoNLL(self.filename)
        self.assertAlmostEqual(0.78, Evaluation.accuracy(wsjFile), 2, "Accuracy should be 0.78");
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
