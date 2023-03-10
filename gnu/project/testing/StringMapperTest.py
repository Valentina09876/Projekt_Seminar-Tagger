'''
Created on Oct 29, 2020

@author: nastasvi
'''
import unittest
from project.tagger.Tagger import Tagger
from project.tagger.data.StringMapper import StringMapper
from project.tagger.model.FeatureExtractors import FeatureExtractors

class StringMapperTest(unittest.TestCase):


    def setUp(self):
        self.filename = "H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\file-onesent.txt"

    #/**
    #   Create int features from String features for a couple of tokens
    #   using the StringMapper.lookup() function
    #   and check that the int are created according to the specification
    # **/

    def testLookup(self):
        sm = StringMapper()
        
        i1 = []
        i1.append(sm.lookup("word=Peter"))
        i1.append(sm.lookup("suffix=er"))
        i1.append(sm.lookup("kap"))
        i1.append(sm.lookup("BOS"))

        i2 = []
        i2.append(sm.lookup("word=denkt"))
        i2.append(sm.lookup("suffix=kt"))
        
        i3 = []
        i3.append(sm.lookup("word=quer"))
        i3.append(sm.lookup("suffix=er"))
        i3.append(sm.lookup("EOS"))

        i1Gold = [1, 2, 3, 4]
        i2Gold = [5, 6]
        i3Gold = [7, 2, 8]

        self.assertEqual(i1Gold, i1)
        self.assertEqual(i2Gold, i2)
        self.assertEqual(i3Gold, i3)

        #// inverse lookups: recover feature name for feature id
        self.assertEqual("word=Peter", sm.inverseLookup(i1[0]))
        self.assertEqual("suffix=er", sm.inverseLookup(i1[1]))
        self.assertEqual("kap", sm.inverseLookup(i1[2]))
        self.assertEqual("BOS", sm.inverseLookup(i1[3]))


    # /**
    #   Test correct serialization of int features
    #  **/
    def testSerialization(self):
        sentences = Tagger.readCoNLL("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\file-onesent.txt")
        fes = FeatureExtractors()
        fes.extractAllFeatures(sentences)
        fes.writeToFile(sentences, "H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\file-onesent.svmmulti")
        fes.stringMapper.toFile("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\file-onesent.fm")

        smDeser = StringMapper.fromFile("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\file-onesent.fm");
        sentencesDeser = FeatureExtractors.readFromFile("H:\\Uni\\Winter Semester 2022 2023\\Projekt _Seminar\\Data\\file-onesent.svmmulti")

       # // check for all tokens that the original and recovered features are identical
        for i in range(len(sentences)):
            for j in range(sentences[i].length()):
                prettyW = self.prettyPrintFeatures(sentences[i].get(j).features, fes.stringMapper)
                prettyWDeser = self.prettyPrintFeatures(sentencesDeser[i].get(j).features, smDeser)
                print("prettyW: {}".format(prettyW))
                self.assertEqual(prettyW, prettyWDeser)


    #   /** given an array of feature IDs, print the original feature strings
    #       e.g. for debugging purposes **/
    def prettyPrintFeatures(self, features, stringMapper):
        print_str = ""
        for feature in features:
            print_str += stringMapper.inverseLookup(feature)
            if feature != features[len(features) - 1]:
                print_str += " "
                
        return print_str



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()