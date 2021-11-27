from model.cardinality import Cardinality
import os

class ModelCompiler:
    def __init__(self, model, classtemplate, genpath):
        self.model = model
        self.classtemplate = classtemplate
        self.genpath = genpath
        self.classpath = genpath + "/classes"
        if not os.path.isdir(self.genpath):
            os.mkdir(self.genpath)
        if not os.path.isdir(self.classpath):
            os.mkdir(self.classpath)

    def compileAll(self, persist=True):
        for _class in self.model.classes().values():
            fpath = self.classpath + "/_" + _class.name() + ".java"
            text = self.classtemplate.templify(self.templateParameters(_class))
            print("ModelCompiler::Create: " + fpath)
            if persist:
                with open(fpath, 'w') as f:
                    f.write(text)
            else:
                print(text)

    def templateParameters(self, _class):
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
        params = {"packageName": "classes",
            "className": _class.name(),
            "attributes": attributes,
            "singleRelations": singleRelations,
            "multiRelations": multiRelations}
        return params