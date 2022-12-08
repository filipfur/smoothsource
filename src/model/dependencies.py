class Dependencies:

    def __init__(self):
        self._dependencies = []

    def add(self, dependency):
        if dependency not in self._dependencies:
            self._dependencies.append(dependency)

    def dependencies(self):
        return self._dependencies