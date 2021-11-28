from modelloader import ModelLoader
from modelcompiler import ModelCompiler
from model.model import Model
import template.template

class smoothsource:

    template = template.template

    def __init__(self):
        self.templates = {}
        self.modelcompiler = None

    def loadModel(self, modelpath):
        model = Model()
        modelloader = ModelLoader(model, modelpath)
        return modelloader.load()

    def createTemplate(self, templatepath):
        tmpl = None
        if templatepath in self.templates:
            tmpl = self.templates[templatepath]
        else:
            tmpl = template.template.Template(templatepath)
            self.templates[templatepath] = tmpl
        return tmpl

    def populateTemplate(self, templatepath, parameters):
        tmpl = self.createTemplate(templatepath)
        tmpl.templify(parameters)

    def createModelCompiler(self, model, classtemplate, genpath):
        if not self.modelcompiler:
            self.modelcompiler = ModelCompiler(model, classtemplate, genpath)
        return self.modelcompiler