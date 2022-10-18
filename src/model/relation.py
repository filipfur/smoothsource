class Relation:

    def __init__(self, _id, leftAssocation, rightAssociation):
        self._id = _id
        self._leftAssociation = leftAssocation
        self._rightAssociation = rightAssociation

    def id(self):
        return self._id

    # Returns the other side of the relation.
    def otherAssociation(self, _class):
        assoc = None

        if self._leftAssociation._class() is _class:
            assoc = self._rightAssociation
        elif self._rightAssociation._class() is _class:
            assoc = self._leftAssociation
        else:
            raise Exception("_class is not associated with relation")

        return assoc

    def leftAssociation(self):
        return self._leftAssociation

    def rightAssociation(self):
        return self._rightAssociation