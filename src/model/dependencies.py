class Dependencies:

    def __init__(self, ownDependency):
        self._dependencies = []
        self._ownDependency = ownDependency

    def add(self, dependency):
        if dependency != self._ownDependency and dependency not in self._dependencies:
            self._dependencies.append(dependency)

    def dependencies(self):
        return self._dependencies