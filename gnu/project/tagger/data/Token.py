'''
Created on Oct 28, 2020

@author: nastasvi
'''



class Token(object):
    '''
    classdocs
    '''

    def __init__(self, word = None, label = None, prediction = None, correctLabelIndex = None,
                 predictedLabelIndex = None, features = [], previous = None, next = None):
        '''
        Constructor
        '''
        self.word = word    #FORM  1
        self.label = label  #POS   4
        self.prediction = prediction #PPOS  5
        
        self.correctLabelIndex = correctLabelIndex
        self.predictedLabelIndex = predictedLabelIndex
        
        self.features = features #FEAT 6
        self.previous = previous
        self.next = next
        
    
    def toString(self):
        word_str = "None"
               
        if self.word != None:
            word_str = "W: " + self.word
            word_str += "\tL: " + Token.getVal(self.label) + "(" + Token.getVal(self.correctLabelIndex) + ")"
            word_str += "\tPL: " + Token.getVal(self.word.prediction) + "(" + Token.getVal(self.predictedLabelIndex) + ")" #
                
        return word_str
        
    
    @staticmethod
    def getVal(val):
        if val == None:
            return "None"
        return "{}".format(val)
        
if __name__ == "__main__":
    token = ""
    Token(token)