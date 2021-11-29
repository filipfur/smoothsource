from template.segment import Segment

TemplateDir = "template"

class Java:
    JavaDir = TemplateDir + "/java"
    ClassTemplate = JavaDir + "/Class.template"
    xtUMLClassTemplate = JavaDir + "/Class.xtuml.template"
    xtUMLClassSelectorTemplate = JavaDir + "/ClassSelector.xtuml.template"

class Template:

    def __init__(self, templatepath):
        self.content = None
        self.templatepath = templatepath
        with open(templatepath, 'r') as f:
            self.content = f.read()
        self.segment = Segment(self.content, root=True)

    def templify(self, parameters):
        self.parameters = parameters
        content = self.segment.populate([parameters], 0)
        return content