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

    def tsType(self, type, package):
        if package == "primitives":
            if type in tsTypeDependencies:
                dep = tsTypeDependencies[type]
                self.dependencies.add(dep)
            if type in tsTypeTranslations:
                return tsTypeTranslations[type]
        elif package != None and package != self.packageName:
            cl = self.model.exClassByKey(package, type)
            dep = self.classDependency(cl)
            self.dependencies.add(dep)
        else:
            cl = self.model.classByName(type)
            dep = self.classDependency(cl)
            self.dependencies.add(dep)
        return type


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

    def classDependency(self, _class):
        otherClassName = _class.name()
        pathToClassFile = None
        if _class.isExternal():
            pathToClassFile = f"../{_class.package()}/{otherClassName.lower()}"
        else:
            pathToClassFile = f"./{otherClassName.lower()}"
        return f"import {'{ ' + otherClassName + ' }'} from \"{pathToClassFile}\""

    def classByPackageAndName(self, package, name):
        cl = None
        if package == None or package == self.packageName:
            cl = self.model.classByName(name)
        else:
            cl = self.model.exClassByKey(package, name)
        return cl

    def templatePayload(self, _class, superClass):
        singleRelations = []
        multiRelations = []
        constructors = []
        operations = []
        self.dependencies = Dependencies()
        for relation in _class.relations():
            otherAssoc = relation.otherAssociation(_class)
            assoc = relation.ourAssociation(_class)
            if assoc.phrase() == "":
                continue
            card = assoc.cardinality()
            otherClassName = otherAssoc._class().name()
            self.dependencies.add(self.classDependency(otherAssoc._class()))
            o = {"className": otherClassName, "phrase": assoc.phrase(), "conditional": (card == Cardinality.Zero_To_One or card == Cardinality.Zero_To_Many)}
            if card == Cardinality.Zero_To_One or card == Cardinality.One:
                singleRelations.append(o)
            else:
                multiRelations.append(o)

        attributes = [{"name": attrib.name(), "type": self.tsType(attrib.type(), attrib.package())} for attrib in _class.attributes()]

        for operation in _class.operations():
            setters = []
            parameters = [f"{x.name()}:{self.tsType(x.type(), x.package())}"
                for x in operation.parameters()]

            for parameter in operation.parameters():
                for attribute in _class.attributes():
                    if parameter.name() == attribute.name():
                        setters.append(f"this.{attribute.name()} = {parameter.name()}")

            o = {"name": operation.name(),
                "type": self.tsType(operation.type(), operation.package()),
                "parameters": ", ".join(parameters),
                "setters": "\n".join(setters),
                "definition": operation.definition(),
                "hash": operation.hash()}
            if operation.name() == "constructor":
                for inherit in _class.inherits():
                    cl = self.classByPackageAndName(inherit.classPackage(), inherit.name())
                    o["superInvoke"] = "super(); // Default invoked since the subclass has no explicit constructor."
                    for superoperation in cl.operations():
                        if superoperation.name() == "constructor":
                            o["parameters"] = ", ".join([f"{x.name()}:{self.tsType(x.type(), x.package())}"
                                for x in superoperation.parameters()] + parameters)
                            o["superInvoke"] = f"super({', '.join([x.name() for x in superoperation.parameters()])});"
                            break
                constructors.append(o)
            else:
                operations.append(o)

        subclasses = []
        for inherit in _class.inherits():
            cl = None
            name = inherit.name()
            if inherit.classPackage() == "primitives":
                name = self.tsType(inherit.name(), inherit.classPackage())
            else:    
                cl = self.classByPackageAndName(inherit.classPackage(), inherit.name())
                dep = self.classDependency(cl)
                self.dependencies.add(dep)
            subclasses.append(name)

        payload = {
            "packageName": self.packageName,
            "className": _class.name(),
            "hash": _class.hash(),
            "pragma": _class.pragma(),
            "attributes": attributes,
            "constructors": constructors,
            "operations": operations,
            "dependencies": "\n".join(self.dependencies.dependencies()),
            "singleRelations": singleRelations,
            "multiRelations": multiRelations,
            "subclasses": ", ".join(subclasses),
        }
        return payload