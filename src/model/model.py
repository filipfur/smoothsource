class Model:

    def __init__(self):
        self._classes = {}
        self._exclasses = {}
        self._relations = []
        self._generalizations = {}
        self._associationLinks = {}

    def addClass(self, _class):
        self._classes[_class.name()] = _class

    def addExClass(self, _class):
        if not _class.package() in self._exclasses:
            self._exclasses[_class.package()] = {}
        self._exclasses[_class.package()][_class.name()] = _class

    def classByName(self, name):
        return self._classes[name] if name in self._classes else None

    def exClassByKey(self, package, name):
        if package in self._exclasses and name in self._exclasses[package]:
            return self._exclasses[package][name]
        return None

    def addRelation(self, relation):
        lClass = relation.leftAssociation()._class().relate(relation)
        rClass = relation.rightAssociation()._class().relate(relation)
        self._relations.append(relation)

    def addGeneralization(self, generalization):
        self._generalizations[generalization.id()] = generalization

    def addAssociationLink(self, assoclink):
        self._associationLinks[assoclink.id()] = assoclink

    def relationById(self, id):
        assert(False) # depreceated
        return self._relations[id]

    def classes(self):
        return self._classes

    def relations(self):
        return self._relations

    def generalizations(self):
        return self._generalizations

    def associationLinks(self):
        return self._associationLinks

    def superClassOf(self, _class):
        superclass = None
        for generalization in self._generalizations.values():
            if generalization.subclass() == _class:
                superclass = generalization.superclass()
                break
        return superclass