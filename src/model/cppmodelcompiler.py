from model.modelcompiler import ModelCompiler
from model.cardinality import Cardinality

class CppModelCompiler(ModelCompiler):

    def __init__(self, model, genpath, removeOld, classhtemplate, classcpptemplate,
            operationcpptemplate):
        ModelCompiler.__init__(self, model, genpath, removeOld)
        self.classhtemplate = classhtemplate
        self.classcpptemplate = classcpptemplate
        self.operationcpptemplate = operationcpptemplate
        self.classpath = genpath + "/classes/"
        self.createdir(self.classpath)

    def compileAll(self, persist=True):
        for _class in self.model.classes().values():
            tparams = self.templatePayload(_class, self.model.superClassOf(_class))

            lowclassname = _class.name().lower()

            fpath = self.classpath + "_" + lowclassname + ".h"
            text = self.classhtemplate.generate(tparams)
            self.create(fpath, text, persist)

            fpath = self.classpath + "_" + lowclassname + ".cpp"
            text = self.classcpptemplate.generate(tparams)
            self.create(fpath, text, persist)

            dpath = self.classpath + lowclassname
            self.createdir(dpath)
            for operation in _class.operations():
                tparams = self.operationPayload(_class, operation)
                fpath = f"{dpath}/{lowclassname}-{operation.name()}.cpp"
                text = self.operationcpptemplate.generate(tparams)
                self.create(fpath, text, persist)

    def operationPayload(self, _class, operation):
        payload = {
            "packageName": "gen",
            "className": _class.name(),
            "name": operation.name(),
            "type": operation.type(),
            "parameters": ", ".join([f"{x.type()} {x.name()}" for x in operation.parameters()]),
            "hash": operation.hash(),
            "definition": operation.definition(),
            "pragma": operation.pragma()
        }
        return payload

    def templatePayload(self, _class, superClass):
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

        attributes = [{"name": attrib.name(), "type": attrib.type()} for attrib in _class.attributes()]

        for operation in _class.operations():
            parameters = ", ".join([f"{x.type()} {x.name()}"
                for x in operation.parameters()])

            operations.append({"name": operation.name(),
                "type": operation.type(),
                "parameters": parameters,
                "definition": operation.definition(),
                "hash": operation.hash()})

        superClasses = []
        if superClass is not None:
            superClasses.append(superClass.name())

        payload = {
            "packageName": "gen",
            "className": _class.name(),
            "hash": "ABC",
            "pragma": "// Enter pragma here",
            "attributes": attributes,
            "operations": operations,
            "singleRelations": singleRelations,
            "multiRelations": multiRelations,
            "superClass": ("" if superClass is None else superClass.name())
        }
        return payload