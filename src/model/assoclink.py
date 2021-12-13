class AssociationLink:

    def __init__(self, uid, _class, relation):
        self._uid = uid
        self.__class = _class
        self._relation = relation

    def uid(self): # TODO: Place uid in base class Unique
        return self._uid

    def _class(self):
        return self.__class

    def relation(self):
        return self._relation