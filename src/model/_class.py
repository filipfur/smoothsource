class Class:

    def __init__(self, uid, name, attributes):
        self._uid = uid
        self._name = name
        self._attributes = attributes
        self._relations = []

    def relate(self, relation):
        if relation not in self._relations:
            self._relations.append(relation)

    def unrelate(self, relation):
        if relation in self._relations:
            self._relations.remove(relation)

    def relations(self):
        return self._relations

    def uid(self):
        return self._uid

    def name(self):
        return self._name

    def attributes(self):
        return self._attributes