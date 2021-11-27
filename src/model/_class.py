class Class:

    def __init__(self, uid, name, attributes):
        self._uid = uid
        self._name = name
        self._attributes = attributes

    def uid(self):
        return self._uid

    def name(self):
        return self._name

    def attributes(self):
        return self._attributes