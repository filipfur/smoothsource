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
        self.classpath = modelpath + "/classes/"
        self.relationpath = modelpath + "/relations/"
        self.definitionpath = modelpath + "/definitions/"
        self.pragmapath = modelpath + "/pragmas/"
        self.generalizationpath = modelpath + "/generalizations/"
        self.assoclinkpath = modelpath + "/association_links/"


    def loadClass(self, fname):
        with open(self.classpath + fname) as f:
            obj = json.load(f)
            attributes = []
            operations = []

            pragma = ""
            with open(self.pragmapath + hash + ".def", 'r') as f:
                pragma = f.read()

            for attribute in obj["attributes"]:
                attributes.append(Class.Attribute(attribute["name"], attribute["type"]))
            for operation in obj["operations"]:
                parameters = []
                for parameter in operation["parameters"]:
                    parameters.append(Class.Parameter(parameter["name"], parameter["type"]))
                hash = operation["hash"]
                definition = ""
                with open(self.definitionpath + hash + ".def", 'r') as f:
                    definition = f.read()
                
                operations.append(Class.Operation(operation["name"], operation["type"], parameters, hash, definition))
            
            self.model.addClass(Class(obj["name"], attributes, operations, obj["hash"], pragma))

    def createAssociation(self, obj):
        return Association(self.model.classByName(obj["className"]), ModelLoader.strToCardinality[obj["cardinality"]], obj["phrase"])

    def loadRelation(self, fname):
        with open(self.relationpath + fname) as f:
            obj = json.load(f)
            lhs = self.createAssociation(obj["left"])
            rhs = self.createAssociation(obj["right"])
            self.model.addRelation(Relation(lhs, rhs))

    def loadGeneralization(self, fname):
        with open(self.generalizationpath + fname) as f:
            obj = json.load(f)
            generalization = Generalization(self.model.classByName(obj["superClass"]), self.model.classByName(obj["subClass"]))
            self.model.addGeneralization(generalization)

    def loadAssociationLink(self, fname):
        with open(self.assoclinkpath + fname) as f:
            obj = json.load(f)
            assoclink = AssociationLink(self.model.classByName(obj["className"]), self.model.relationById(obj["relation"]))
            self.model.addAssociationLink(assoclink)

    def loadPath(self, path, method):
        if os.path.isdir(path):
            for fpath in os.listdir(path):
                method(fpath)

    def load(self):
        self.loadPath(self.classpath, self.loadClass)
        self.loadPath(self.relationpath, self.loadRelation)
        self.loadPath(self.generalizationpath, self.loadGeneralization)
        self.loadPath(self.assoclinkpath, self.loadAssociationLink)