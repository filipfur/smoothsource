import os
import json

from model.model import Model
from model._class import Class
from model.relation import Relation
from model.association import Association
from model.cardinality import Cardinality

class ModelLoader:

    strToCardinality = {"0..1": Cardinality.Zero_To_One, "1": Cardinality.One, "*": Cardinality.Zero_To_Many, "1..*": Cardinality.One_To_Many}


    def __init__(self, model, modelpath):
        self.model = Model()
        self.classpath = modelpath + "/class/"
        self.relationpath = modelpath + "/relation/"


    def loadClass(self, uid):
        with open(self.classpath + uid) as f:
            obj = json.load(f)
            self.model.addClass(Class(obj["uid"], obj["name"], obj["attributes"]))

    def createAssociation(self, obj):
        return Association(self.model.classByUid(obj["class"]), ModelLoader.strToCardinality[obj["cardinality"]], obj["phrase"])

    def loadRelation(self, uid):
        with open(self.relationpath + uid) as f:
            obj = json.load(f)
            lobj = obj["lhs"]
            robj = obj["rhs"]
            lhs = self.createAssociation(obj["lhs"])
            rhs = self.createAssociation(obj["rhs"])
            self.model.addRelation(Relation(obj["uid"], obj["id"], lhs, rhs))

    def load(self):
        for fpath in os.listdir(self.classpath):
            self.loadClass(fpath)
        for fpath in os.listdir(self.relationpath):
            self.loadRelation(fpath)
        return self.model