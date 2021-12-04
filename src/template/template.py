from template.segment import Segment

TemplateDir = "template"

class Java:
    JavaDir = TemplateDir + "/java"
    ClassTemplate = JavaDir + "/Class.template"
    xtUMLClassTemplate = JavaDir + "/Class.smoothsource"
    xtUMLClassSelectorTemplate = JavaDir + "/ClassSelector.smoothsource"

class Template:

    def __init__(self, templatepath):
        self.content = None
        self.templatepath = templatepath
        with open(templatepath, 'r') as f:
            self.content = f.read()
        self.segment = Segment(self.content, root=True)

    def generate(self, payload):
        content = self.segment.populate([payload], 0)
        return content