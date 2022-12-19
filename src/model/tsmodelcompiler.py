from model.modelcompiler import ModelCompiler
from model.cardinality import Cardinality
from model.dependencies import Dependencies
import os

tsTypeTranslations = {
    "void": "void",
    "boolean": "boolean",
    "integer": "number",
    "real": "number",
    "character": "string",
    "string": "string"
}

tsTypeDependencies = {
#    "string": "#include <string>"
}

def tsType(type, dependencies):
    if type in tsTypeDependencies:
        dep = tsTypeDependencies[type]
        dependencies.add(dep)
    if type in tsTypeTranslations:
        return tsTypeTranslations[type]
    return type

class TypescriptModelCompiler(ModelCompiler):

    def __init__(self, model, genpath, removeOld, packageName, classtemplate, classdtemplate):
        ModelCompiler.__init__(self, model, genpath)
        self.packagepath = os.path.join(genpath, packageName)
        if removeOld:
            self.rmdir(self.packagepath)
        self.classtemplate = classtemplate
        self.classdtemplate = classdtemplate
        self.packageName = packageName
        self.createdir(self.packagepath)

    def compileAll(self, persist=True):
        for _class in self.model.classes().values():
            tparams = self.templatePayload(_class, self.model.superClassOf(_class))

            lowclassname = _class.name().lower()

            fpath = os.path.join(self.packagepath, lowclassname + ".ts")
            text = self.classtemplate.generate(tparams)
            self.create(fpath, text, persist)

            fpath = os.path.join(self.packagepath, lowclassname + ".d.ts")
            text = self.classdtemplate.generate(tparams)
            self.create(fpath, text, persist)

    def templatePayload(self, _class, superClass):
        singleRelations = []
        multiRelations = []
        constructors = []
        operations = []
        dependencies = Dependencies()
        for relation in _class.relations():
            otherAssoc = relation.otherAssociation(_class)
            assoc = relation.ourAssociation(_class)
            if assoc.phrase() == "":
                continue
            card = assoc.cardinality()
            otherClassName = otherAssoc._class().name()
            pathToClassFile = None
            if otherAssoc._class().isExternal():
                pathToClassFile = f"../{otherAssoc._class().package()}/{otherClassName.lower()}"
            else:
                pathToClassFile = f"./{otherClassName.lower()}"
            dependencies.add(f"import {'{ ' + otherClassName + ' }'} from \"{pathToClassFile}\"")
            o = {"className": otherClassName, "phrase": assoc.phrase(), "conditional": (card == Cardinality.Zero_To_One or card == Cardinality.Zero_To_Many)}
            print(o)
            if card == Cardinality.Zero_To_One or card == Cardinality.One:
                singleRelations.append(o)
            else:
                multiRelations.append(o)

        attributes = [{"name": attrib.name(), "type": tsType(attrib.type(), dependencies)} for attrib in _class.attributes()]


        for operation in _class.operations():
            setters = []
            parameters = ", ".join([f"{x.name()}:{tsType(x.type(), dependencies)}"
                for x in operation.parameters()])

            for parameter in operation.parameters():
                for attribute in _class.attributes():
                    if parameter.name() == attribute.name():
                        setters.append(f"this.{attribute.name()} = {parameter.name()}")

            o = {"name": operation.name(),
                "type": tsType(operation.type(), dependencies),
                "parameters": parameters,
                "setters": "\n".join(setters),
                "definition": operation.definition(),
                "hash": operation.hash()}
            if operation.name() == "constructor":
                constructors.append(o)
            else:
                operations.append(o)

        superClasses = []
        if superClass is not None:
            superClasses.append(superClass.name())

        payload = {
            "packageName": self.packageName,
            "className": _class.name(),
            "hash": _class.hash(),
            "pragma": _class.pragma(),
            "attributes": attributes,
            "constructors": constructors,
            "operations": operations,
            "dependencies": "\n".join(dependencies.dependencies()),
            "singleRelations": singleRelations,
            "multiRelations": multiRelations,
            "superClass": ("" if superClass is None else superClass.name())
        }
        return payload