class Class:

    class Property:
        def __init__(self, name, _type):
            self._name = name
            self._type = _type
        def name(self):
            return self._name
        def type(self):
            return self._type

    class Attribute(Property):
        def __init__(self, name, _type):
            Class.Property.__init__(self, name, _type)

    class Parameter(Property):
        def __init__(self, name, _type):
            Class.Property.__init__(self, name, _type)

    class Operation(Property):
        def __init__(self, name, _type, parameters, hash, definition):
            Class.Property.__init__(self, name, _type)
            self._parameters = parameters
            self._hash = hash
            self._definition = definition
        def hash(self):
            return self._hash
        def parameters(self):
            return self._parameters
        def definition(self):
            return self._definition

    def __init__(self, name, attributes, operations):
        self._name = name
        self._attributes = attributes
        self._operations = operations
        self._relations = []

    def relate(self, relation):
        if relation not in self._relations:
            self._relations.append(relation)

    def unrelate(self, relation):
        if relation in self._relations:
            self._relations.remove(relation)

    def relations(self):
        return self._relations

    def name(self):
        return self._name

    def attributes(self):
        return self._attributes

    def operations(self):
        return self._operations