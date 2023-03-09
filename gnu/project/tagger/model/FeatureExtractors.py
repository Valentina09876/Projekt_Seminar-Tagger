"""

"""

from project.tagger.data.Token import Token
from project.tagger.data.Sentence import Sentence
from project.tagger.data.StringMapper import StringMapper


class FeatureExtractors(object):
    """
    Extract features of a token
    """

    def __init__(self):
        """
        Constructor
        A FeatureExtractor-Object has a string Mapper
        """
        self.stringMapper = StringMapper()

    def extractPrevWord(self, token: Token):
        """
        Extract the word form of the previous Token

        @param token: word form
        """

        token.features.append(self.stringMapper.lookup('previous: ' + token.previous.word))

    def extractCurrentWord(self, token: Token):
        """
        Extract current word from of the Token.

        @param token: word form
        """
        token.features.append(self.stringMapper.lookup('word:' + token.word))

    def extractNextWord(self, token: Token):
        """
        Extract the word form of the next Token.

        @param token: word form
        """

        token.features.append(self.stringMapper.lookup('next: ' + token.next.word))

    def extractSuffices(self, token: Token):
        """
        Extract suffices from the Token in a range from 1 to 5.

        @param token: word form
        """

        if len(token.word) <= 5:
            token.features += [self.stringMapper.lookup('suffix: ' + token.word[-i:]) for i in range(1, len(token.word))]
        else:
            token.features += [self.stringMapper.lookup('suffix: ' + token.word[-i:]) for i in range(1, 6)]

    def extractCurrentPOS(self, token: Token):
        """
        Extract Part-Of-Speach from the Token

        @param token: word form
        """

        token.features.append(self.stringMapper.lookup('POS: ' + token.label))

    def extractPreviousPOS(self, token: Token):
        """
        Extract Part-Of-Speach of the previous Token.

        @param token: word form
        """

        token.features.append(self.stringMapper.lookup('prevPOS: ' + token.previous.label))

    def extractNextPOS(self, token: Token):
        """
        Extract Part-Of-Speach of the next Token.

        @param token: word form
        """

        token.features.append(self.stringMapper.lookup('nextPOS: ' + token.next.label))

    def extractFeatures(self, token: Token):
        """
        Extract all features from the Token.

        @param token: word form
        """
        # initialize an empty list for the features solve some issues
        token.features = []

        self.extractCurrentWord(token)
        self.extractPrevWord(token)
        self.extractNextWord(token)
        self.extractSuffices(token)

        # new features
        # self.extractCurrentPOS(token)
        self.extractPreviousPOS(token)
        self.extractNextPOS(token)

    def extractAllFeatures(self, sentences: list[Sentence]):
        """
        Extract all features from a list of sentences.

        @param sentences:  a list of sentences
        """

        for sent in sentences:
            for token in sent.tokens:
                self.extractFeatures(token)

    def writeToFile(self, sentences: list[Sentence], file_name: str):
        """
        Save sentences in svm-milticlass file.

        @param sentences: list of sentences
        @param file_name: path of the svm-multiclass file to save teh sentences in
        """

        end_of_sent = self.stringMapper.lookup('EOS')

        with open(file_name, "w") as output_file:
            for sentence in sentences:
                for token in sentence.tokens:
                    for feature in token.features:
                        output_file.write(str(feature) + ':1 ')

                    output_file.write('#')
                    if self.stringMapper.lookup(token.next.word) == end_of_sent:
                        output_file.write('EOS')
                    output_file.write('\n')

    @staticmethod
    def readFromFile(file_name: str) -> list[Sentence]:
        """
        Reads a svm-multiclass file and returns a list of sentences (previous example readCoNLL).

        @param file_name: name of the svm-multiclass file to read
        @return: list of sentences
        """

        sentences = []
        with open(file_name, "r") as input_file:

            sentence = []
            while line := input_file.readline():

                features = [token.split(':')[0] for token in line.split()]

                sentence.append(Token(
                    word=int(features[0]),
                    previous=int(features[1]),
                    next=int(features[2]),
                    features=[int(feat) for feat in features[:-1]]
                ))

                if features[-1] == '#EOS':
                    sentences.append(Sentence(sentence))
                    sentence = []

        return sentences



