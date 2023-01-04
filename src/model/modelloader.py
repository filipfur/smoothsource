import os
import json

from model.model import Model
from model._class import Class
from model.relation import Relation
from model.association import Association
from model.cardinality import Cardinality
from model.generalization import Generalization
from model.assoclink import AssociationLink

class ModelLoader:

    strToCardinality = {"0..1": Cardinality.Zero_To_One, "1": Cardinality.One, "*": Cardinality.Zero_To_Many, "1..*": Cardinality.One_To_Many}


    def __init__(self, model, modelpath):
        self.model = model
        self.modelpath = modelpath
        self.definitionpath = modelpath + "/definitions/"
        self.pragmapath = modelpath + "/pragmas/"


    def loadClass(self, fpath, package=None):
        cl = None
        with open(fpath) as f:
            obj = json.load(f)
            inherits = []
            attributes = []
            operations = []

            for inherit in obj["inherits"]:
                inherits.append(Class.Inheritance(inherit["name"]["name"], inherit["name"]["package"], inherit["type"]["name"], inherit["type"]["package"]))
            for attribute in obj["attributes"]:
                attributes.append(Class.Attribute(attribute["name"], attribute["type"]["name"], attribute["type"]["package"],
                    attribute["identifier"] if "identifier" in attribute else False))
            for operation in obj["operations"]:
                parameters = []
                for parameter in operation["parameters"]:
                    parameters.append(Class.Parameter(parameter["name"], parameter["type"]["name"], parameter["type"]["package"]))
                hash = operation["hash"]
                definition = ""
                if package == None:
                    with open(self.definitionpath + hash + ".def", 'r') as f:
                        definition = f.read()
                operations.append(Class.Operation(operation["name"], operation["type"]["name"], operation["type"]["package"], parameters, hash, definition))
            
            hash = obj["hash"]
            pragma = ""
            if package == None:
                with open(self.pragmapath + hash + ".def", 'r') as f:
                    pragma = f.read()
            
            cl = Class(obj["name"], inherits, attributes, operations, hash, pragma, package)
            if package == None:
                self.model.addClass(cl)
            else:
                self.model.addExClass(cl)
        return cl

    def createAssociation(self, obj):
        cl = None
        if "package" in obj:
            cl = self.model.exClassByKey(obj["package"], obj["className"])
            if cl == None:
                cl = self.loadClass(os.path.join(os.path.join(self.modelpath, "..", obj["package"]), "classes", obj["className"] + ".json"), obj["package"])
        else:
            cl = self.model.classByName(obj["className"])
        return Association(cl, ModelLoader.strToCardinality[obj["cardinality"]], obj["phrase"])

    def loadRelation(self, fpath):
        with open(fpath) as f:
            obj = json.load(f)
            lhs = self.createAssociation(obj["left"])
            rhs = self.createAssociation(obj["right"])
            self.model.addRelation(Relation(lhs, rhs))

    def loadPath(self, path, method):
        if os.path.isdir(path):
            for fpath in os.listdir(path):
                method(os.path.join(path, fpath))

    def load(self):
        self.loadPath(os.path.join(self.modelpath, "classes"), self.loadClass)
        self.loadPath(os.path.join(self.modelpath, "relations"), self.loadRelation)