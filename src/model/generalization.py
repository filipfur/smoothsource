class Generalization:

    def __init__(self, uid, superclass, subclass):
        self._uid = uid
        self._superclass = superclass
        self._subclass = subclass

    def uid(self):
        return self._uid

    def superclass(self):
        return self._superclass

    def subclass(self):
        return self._subclass