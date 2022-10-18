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
        self.generalizationpath = modelpath + "/generalizations/"
        self.assoclinkpath = modelpath + "/association_links/"


    def loadClass(self, fname):
        with open(self.classpath + fname) as f:
            obj = json.load(f)
            self.model.addClass(Class(obj["name"], obj["attributes"]))

    def createAssociation(self, obj):
        return Association(self.model.classByName(obj["class"]), ModelLoader.strToCardinality[obj["cardinality"]], obj["phrase"])

    def loadRelation(self, fname):
        with open(self.relationpath + fname) as f:
            obj = json.load(f)
            lhs = self.createAssociation(obj["left"])
            rhs = self.createAssociation(obj["right"])
            self.model.addRelation(Relation(obj["id"], lhs, rhs))

    def loadGeneralization(self, fname):
        with open(self.generalizationpath + fname) as f:
            obj = json.load(f)
            generalization = Generalization(self.model.classByName(obj["superClass"]), self.model.classByName(obj["subClass"]))
            self.model.addGeneralization(generalization)

    def loadAssociationLink(self, fname):
        with open(self.assoclinkpath + fname) as f:
            obj = json.load(f)
            assoclink = AssociationLink(self.model.classByName(obj["class"]), self.model.relationById(obj["relation"]))
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