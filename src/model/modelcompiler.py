from model.cardinality import Cardinality
import os

class ModelCompiler:
    def __init__(self, model, classtemplate, selectortemplate, genpath):
        self.model = model
        self.classtemplate = classtemplate
        self.selectortemplate = selectortemplate
        self.genpath = genpath
        self.classpath = genpath + "/classes"
        self.selectorpath = genpath + "/selectors"
        if not os.path.isdir(self.genpath):
            os.mkdir(self.genpath)
        if not os.path.isdir(self.classpath):
            os.mkdir(self.classpath)
        if not os.path.isdir(self.selectorpath):
            os.mkdir(self.selectorpath)

    def create(self, fpath, text, persist):
        print("ModelCompiler::Create: " + fpath)
        if persist:
            with open(fpath, 'w') as f:
                f.write(text)
        else:
            print(text)

    def compileAll(self, persist=True):
        for _class in self.model.classes().values():
            tparams = self.templatePayload(_class)

            fpath = self.classpath + "/_" + _class.name() + ".java"
            text = self.classtemplate.generate(tparams)
            self.create(fpath, text, persist)

            fpath = self.selectorpath + "/" + _class.name() + "Selector.java"
            text = self.selectortemplate.generate(tparams)
            self.create(fpath, text, persist)
            

    def templatePayload(self, _class):
        attributes = []
        singleRelations = []
        multiRelations = []
        for relation in _class.relations():
            otherAssoc = relation.otherAssociation(_class)
            card = otherAssoc.cardinality()
            o = {"relationId": relation.id(), "relatedClassName": otherAssoc._class().name()}
            if card == Cardinality.Zero_To_One or card == Cardinality.One:
                singleRelations.append(o)
            else:
                multiRelations.append(o)
        classAttribs = _class.attributes()
        for aName in classAttribs:
            attributes.append({"attributeName": aName, "attributeType": classAttribs[aName]})
        params = {"packageName": "gen",
            "imports": [],# [{"classPath": classPath} for classPath in ["util.AttributeMatcher", "util.RelationManager"]],
            "userClassPath": "user",
            "className": _class.name(),
            "attributes": attributes,
            "singleRelations": singleRelations,
            "multiRelations": multiRelations}
        return params