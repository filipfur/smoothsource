from smoothsource import smoothsource
from model.model import Model
from model.modelloader import ModelLoader
from model.modelcompiler import ModelCompiler


def main():
    model = Model()
    modelloader = ModelLoader(model, "test/xtuml")
    modelloader.load()

    classtemplate = smoothsource.createTemplate(smoothsource.template.Java.xtUMLClassTemplate)
    selectortemplate = smoothsource.createTemplate(smoothsource.template.Java.xtUMLClassSelectorTemplate)

    modelcompiler = ModelCompiler(model, classtemplate, selectortemplate, "test/xtuml/src/gen")

    modelcompiler.compileAll(persist=True)


if __name__ == "__main__":
    main()