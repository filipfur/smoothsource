class Generalization:

    def __init__(self, superclass, subclass):
        self._superclass = superclass
        self._subclass = subclass

    def superclass(self):
        return self._superclass

    def subclass(self):
        return self._subclass