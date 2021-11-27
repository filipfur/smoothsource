class Association:

    def __init__(self, _class, cardinality, phrase):
        self.__class = _class
        self._cardinality = cardinality
        self._phrase = phrase

    def _class(self):
        return self.__class

    def cardinality(self):
        return self._cardinality

    def phrase(self):
        return self._phrase