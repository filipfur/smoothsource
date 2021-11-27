class Model:

    def __init__(self):
        self._classes = {}
        self._relations = {}

    def addClass(self, _class):
        self._classes[_class.uid()] = _class

    def classByUid(self, uid):
        return self._classes[uid]

    def addRelation(self, relation):
        self._relations[relation.uid()] = relation

    def relationByUid(self, uid):
        return self.relations[uid]

    def classes(self):
        return self._classes

    def relations(self):
        return self._relations