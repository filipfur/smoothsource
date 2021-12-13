class Model:

    def __init__(self):
        self._classes = {}
        self._relations = {}
        self._generalizations = {}
        self._associationLinks = {}

    def addClass(self, _class):
        self._classes[_class.uid()] = _class

    def classByUid(self, uid):
        return self._classes[uid]

    def addRelation(self, relation):
        lClass = relation.leftAssociation()._class().relate(relation)
        rClass = relation.rightAssociation()._class().relate(relation)
        self._relations[relation.uid()] = relation

    def addGeneralization(self, generalization):
        self._generalizations[generalization.uid()] = generalization

    def addAssociationLink(self, assoclink):
        self._associationLinks[assoclink.uid()] = assoclink

    def relationByUid(self, uid):
        return self._relations[uid]

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