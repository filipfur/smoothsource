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
        self.classpath = modelpath + "/class/"
        self.relationpath = modelpath + "/relation/"
        self.generalizationpath = modelpath + "/generalization/"
        self.assoclinkpath = modelpath + "/association_link/"


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

    def loadGeneralization(self, uid):
        with open(self.generalizationpath + uid) as f:
            obj = json.load(f)
            generalization = Generalization(obj["uid"], self.model.classByUid(obj["superClass"]), self.model.classByUid(obj["subClass"]))
            self.model.addGeneralization(generalization)

    def loadAssociationLink(self, uid):
        with open(self.assoclinkpath + uid) as f:
            obj = json.load(f)
            assoclink = AssociationLink(obj["uid"], self.model.classByUid(obj["class"]), self.model.relationByUid(obj["relation"]))
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