class AssociationLink:

    def __init__(self, _class, relation):
        self.__class = _class
        self._relation = relation

    def _class(self):
        return self.__class

    def relation(self):
        return self._relation