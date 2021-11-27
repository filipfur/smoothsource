from modelloader import ModelLoader
from model.model import Model
from templateparser import TemplateParser

class smoothsource:

    def loadModel(modelpath):
        model = Model()
        modelloader = ModelLoader(model, modelpath)
        return modelloader.load()

    def parseTemplate(templatepath):
        parser = TemplateParser(templatepath)
        parser.parse()