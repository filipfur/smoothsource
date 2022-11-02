from model.modelcompiler import ModelCompiler
from model.cardinality import Cardinality
import os

cppTypeTranslations = {
    "void": "void",
    "boolean": "bool",
    "integer": "int",
    "real": "float",
    "character": "char",
    "string": "std::string"
}

cppTypeDependencies = {
    "string": "#include <string>"
}

def cppType(type, dependencies):
    if type in cppTypeDependencies:
        dep = cppTypeDependencies[type]
        if dep not in dependencies:
            dependencies.append(dep)
    if type in cppTypeTranslations:
        return cppTypeTranslations[type]
    return type

class CppModelCompiler(ModelCompiler):

    def __init__(self, model, genpath, removeOld, packageName, classhtemplate, classcpptemplate,
            operationcpptemplate):
        ModelCompiler.__init__(self, model, genpath)
        self.packagepath = os.path.join(genpath, packageName)
        if removeOld:
            self.rmdir(self.packagepath)
        self.classhtemplate = classhtemplate
        self.classcpptemplate = classcpptemplate
        self.operationcpptemplate = operationcpptemplate
        self.packageName = packageName
        self.createdir(self.packagepath)

    def compileAll(self, persist=True):
        for _class in self.model.classes().values():
            tparams = self.templatePayload(_class, self.model.superClassOf(_class))

            lowclassname = _class.name().lower()

            fpath = os.path.join(self.packagepath, lowclassname + ".h")
            text = self.classhtemplate.generate(tparams)
            self.create(fpath, text, persist)

            fpath = os.path.join(self.packagepath, lowclassname + ".cpp")
            text = self.classcpptemplate.generate(tparams)
            self.create(fpath, text, persist)

            #dpath = os.path.join(self.packagepath, lowclassname)
            #self.createdir(dpath)
            #for operation in _class.operations():
            #    tparams = self.operationPayload(_class, operation)
            #    fpath = os.path.join(f"{lowclassname}-{operation.name()}.cpp")
            #    text = self.operationcpptemplate.generate(tparams)
            #    self.create(fpath, text, persist)

    #def operationPayload(self, _class, operation):
    #    payload = {
    #        "packageName": self.packageName,
    #        "className": _class.name(),
    #        "name": operation.name(),
    #        "type": operation.type(),
    #        "parameters": ", ".join([f"{x.type()} {x.name()}" for x in operation.parameters()]),
    #        "hash": operation.hash(),
    #        "definition": operation.definition(),
    #        "pragma": _class.pragma()
    #    }
    #    return payload

    def templatePayload(self, _class, superClass):
        singleRelations = []
        multiRelations = []
        operations = []
        dependencies = []
        for relation in _class.relations():
            otherAssoc = relation.otherAssociation(_class)
            card = otherAssoc.cardinality()
            o = {"relatedClassName": otherAssoc._class().name()}
            if card == Cardinality.Zero_To_One or card == Cardinality.One:
                singleRelations.append(o)
            else:
                multiRelations.append(o)

        attributes = [{"name": attrib.name(), "type": cppType(attrib.type(), dependencies)} for attrib in _class.attributes()]

        for operation in _class.operations():
            parameters = ", ".join([f"{cppType(x.type(), dependencies)} {x.name()}"
                for x in operation.parameters()])

            operations.append({"name": operation.name(),
                "type": cppType(operation.type(), dependencies),
                "parameters": parameters,
                "definition": operation.definition(),
                "hash": operation.hash()})

        superClasses = []
        if superClass is not None:
            superClasses.append(superClass.name())

        payload = {
            "packageName": self.packageName,
            "className": _class.name(),
            "hash": _class.hash(),
            "pragma": _class.pragma(),
            "attributes": attributes,
            "operations": operations,
            "dependencies": "\n".join(dependencies),
            "singleRelations": singleRelations,
            "multiRelations": multiRelations,
            "superClass": ("" if superClass is None else superClass.name())
        }
        return payload