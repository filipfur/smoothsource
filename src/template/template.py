from template.segment import Segment

import os

TemplateDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../template")

class Java:
    JavaDir = os.path.join(TemplateDir, "java")
    ClassTemplate = os.path.join(JavaDir, "Class.template")
    xtUMLClassTemplate = os.path.join(JavaDir, "Class.smoothsource")
    xtUMLClassSelectorTemplate = os.path.join(JavaDir, "ClassSelector.smoothsource")

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