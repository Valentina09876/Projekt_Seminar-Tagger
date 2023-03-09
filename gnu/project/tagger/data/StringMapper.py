"""
Aufgabe 3
Festlegung der Identifikations-Indizes

Das erste Merkmal, das generiert wird erhält die Identifikations Nummer 1, für jedes weitere
genrierte Merkmal erhöht sich diese Identifikations nummer um 1. wenn ein Merkmal bereits
mit seiner Identifikations nummer generiert wurde wird diese beibehalten.

"""

class StringMapper(object):
    """
    Class to Map the features of a token/Sentence

    """
    def __init__(self):
        """
        Constructor

        Each Instance of a StringMapper has a List with its features and their indices
        """
        self.feature_dict = {}
        self.feature_index = 0

    def lookup(self, feature: str):
        """
        looks for a given feature and returns its index

        if the index for that feature does not exist it generates a new index

        """
        if feature not in self.feature_dict:
            self.feature_index += 1
            self.feature_dict.update({feature: self.feature_index})

        return self.feature_dict[feature]





    def inverseLookup(self, feature_index: int):
        """
        it returns the feature for its given index.

        @param: feature_index, the index for which feature we are looking for
        """
        for feature, index in self.feature_dict.items():
            if feature_index == index:
                return feature

    def toFile(self, filename: str):
        """
        Serialize the String-Mapper saving the feature-dictionary into an external file.

        @param filename, path of the file you want to save the feature dictionary

        """

        with open(filename, "w") as output_file:
            for token in list(self.feature_dict.keys()):
                output_file.write(token + '\n')


    def fromFile(filename: str):
        """
        Read the serialized String-Mapper from the file.

        @param filename: path of the file to read
        @return: StringMapper-Object with feature list and index
        """

        feature_dict = {}
        feature_index = 0

        with open(filename, "r") as input_file:

            while feature := input_file.readline():
                feature_index += 1
                feature_dict.update({feature.removesuffix('\n'): feature_index})

        stringMapper = StringMapper()
        stringMapper.feature_dict = feature_dict
        stringMapper.feature_index = feature_index

        return stringMapper