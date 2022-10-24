from model.modelcompiler import ModelCompiler
from model.cardinality import Cardinality

class CppModelCompiler(ModelCompiler):

    def __init__(self, model, genpath, removeOld, classhtemplate, classcpptemplate):
        ModelCompiler.__init__(self, model, genpath, removeOld)
        self.classhtemplate = classhtemplate
        self.classcpptemplate = classcpptemplate
        self.classpath = genpath + "/classes"
        self.createdir(self.classpath)

    def compileAll(self, persist=True):
        for _class in self.model.classes().values():
            tparams = self.templatePayload(_class, self.model.superClassOf(_class))

            fpath = self.classpath + "/_" + _class.name().lower() + ".h"
            text = self.classhtemplate.generate(tparams)
            self.create(fpath, text, persist)

            fpath = self.classpath + "/_" + _class.name().lower() + ".cpp"
            text = self.classcpptemplate.generate(tparams)
            self.create(fpath, text, persist)
        
    def templatePayload(self, _class, superClass):
        attributes = []
        singleRelations = []
        multiRelations = []
        operations = []
        for relation in _class.relations():
            otherAssoc = relation.otherAssociation(_class)
            card = otherAssoc.cardinality()
            o = {"relatedClassName": otherAssoc._class().name()}
            if card == Cardinality.Zero_To_One or card == Cardinality.One:
                singleRelations.append(o)
            else:
                multiRelations.append(o)
        classAttribs = _class.attributes()
        for attrib in classAttribs:
            attributes.append({"attributeName": attrib["name"], "attributeType": attrib["type"]})

        for operation in _class.operations():
            parameters = ""
            delim = ""
            for param in operation["parameters"]: # This could be done in a file.
                parameters += delim + param["type"] + " " + param["name"]
                delim = ", "

            operations.append({"operationName": operation["name"],
                "operationType": operation["type"],
                "operationParameters": parameters,
                "operationImplementation": "{{IMPL_ajhdADASDhjkasd}}"})

        superClasses = []
        if superClass is not None:
            superClasses.append(superClass.name())

        payload = {
            "packageName": "gen",
            "imports": [],# [{"classPath": classPath} for classPath in ["util.AttributeMatcher", "util.RelationManager"]],
            "userClassPath": "user",
            "className": _class.name(),
            "attributes": attributes,
            "operations": operations,
            "singleRelations": singleRelations,
            "multiRelations": multiRelations,
            "superClass": ("" if superClass is None else superClass.name())
        }
        return payload