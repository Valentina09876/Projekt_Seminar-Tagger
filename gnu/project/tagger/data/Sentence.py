'''
Created on Oct 28, 2020

@author: nastasvi
'''

class Sentence(object):
    '''
    classdocs
    '''


    def __init__(self, tokens = []):
        '''
        Constructor
        '''
        self.tokens = tokens
        
    def length(self):
        return len(self.tokens)
    
    
    def isEmpty(self):
        return len(self.tokens) == 0
    
    
    def add(self, token):
        self.tokens.append(token)
        
        
    def get(self, i):
        return self.tokens[i]
    
    
    def toString(self):
        sent = ""
        for x in self.tokens:
            #sent += "{} ({})\t".format(x.word, x.features)
            sent += "{} ".format(x.word)
        return sent



if __name__ == "__main__":
    list_tokens = ["Hello", "what", "building", "rabbit", "uncle"]  #strings keine tokens
    new_sentence = Sentence(list_tokens)  #init methode
    list_sentence = ["Hello world!", "The term originally referred to messages sent using the Short Message Service (SMS).",
                     "It has grown beyond alphanumeric text to include multimedia messages using the Multimedia Messaging Service (MMS)."]
    sentence = Sentence(list_sentence)
    print(sentence.tokens)
    print(sentence.length())
    print(sentence.isEmpty())
    print(sentence.toString())


    print(new_sentence.tokens)
    print(new_sentence.length())
    print(new_sentence.isEmpty())
    print(new_sentence.toString())

