from smoothsource import smoothsource
from model.model import Model
from model.modelloader import ModelLoader
from model.modelcompiler import ModelCompiler
import getopt
import sys

def translate(modelpath, genpath):
    model = Model()
    modelloader = ModelLoader(model, modelpath)
    modelloader.load()
    classtemplate = smoothsource.createTemplate(smoothsource.template.Java.xtUMLClassTemplate)
    selectortemplate = smoothsource.createTemplate(smoothsource.template.Java.xtUMLClassSelectorTemplate)
    modelcompiler = ModelCompiler(model, classtemplate, selectortemplate, genpath)
    modelcompiler.compileAll(persist=True)
    return True

def main():
    opts, args = getopt.getopt(sys.argv[1:], "vm:o:", ["version", "model-path=", "output-dir="])
    modelpath = "test/xtuml/cars"
    genpath = "test/xtuml/src/gen"

    print(opts)
    for opt, arg in opts:
        if opt in ("-m", "-model-path="):
            modelpath = arg
        elif opt in ("-o", "-output-dir="):
            genpath = arg

    print("modelpath=%s" % modelpath)
    print("genpath=%s" % genpath)

    translate(modelpath, genpath)


if __name__ == "__main__":
    main()