class ClassRef:

    def __init__(self, name, package):
        self._name = name
        self._package = package

    def name(self):
        return self._name

    def package(self):
        return self._package

    def isExternal(self):
        return True

    def relate(self, relation):
        pass

    def unrelate(self, relation):
        pass