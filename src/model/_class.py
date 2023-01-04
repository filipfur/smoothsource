class Class:

    class Property:
        def __init__(self, name, _type, _package):
            self._name = name
            self._type = _type
            self._package = _package
        def name(self):
            return self._name
        def type(self):
            return self._type
        def package(self):
            return self._package

    class Attribute(Property):
        def __init__(self, name, _type, _package, identifier):
            Class.Property.__init__(self, name, _type, _package)
            self._identifier = identifier

        def isIdentifier(self):
            return self._identifier

    class Parameter(Property):
        def __init__(self, name, _type, _package):
            Class.Property.__init__(self, name, _type, _package)

    class Operation(Property):
        def __init__(self, name, _type, _package, parameters, hash, definition):
            Class.Property.__init__(self, name, _type, _package)
            self._parameters = parameters
            self._hash = hash
            self._definition = definition
        def hash(self):
            return self._hash
        def parameters(self):
            return self._parameters
        def definition(self):
            return self._definition

    class Inheritance(Property):
        def __init__(self, name, classPackage, _type, _package):
            Class.Property.__init__(self, name, _type, _package)
            self._classPackage = classPackage
        def classPackage(self):
            return self._classPackage

    def __init__(self, name, inherits, attributes, operations, hash, pragma, package):
        self._name = name
        self._inherits = inherits
        self._attributes = attributes
        self._operations = operations
        self._relations = []
        self._hash = hash
        self._pragma = pragma
        self._package = package

    def relate(self, relation):
        if relation not in self._relations:
            self._relations.append(relation)

    def unrelate(self, relation):
        if relation in self._relations:
            self._relations.remove(relation)

    def inherit(self, _class):
        self._inherits.append(_class)

    def inherits(self):
        return self._inherits

    def relations(self):
        return self._relations

    def name(self):
        return self._name

    def attributes(self):
        return self._attributes

    def operations(self):
        return self._operations

    def pragma(self):
        return self._pragma

    def hash(self):
        return self._hash
    
    def package(self):
        return self._package

    def isExternal(self):
        return self._package != None