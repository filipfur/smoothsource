class Relation:

    def __init__(self, uid, _id, leftAssocation, rightAssociation):
        self._uid = uid
        self._id = _id
        self._leftAssociation = leftAssocation
        self._rightAssociation = rightAssociation

    def uid(self):
        return self._uid

    def id(self):
        return self._id

    def leftAssociation(self):
        return self._leftAssociation

    def rightAssociation(self):
        return self._rightAssociation