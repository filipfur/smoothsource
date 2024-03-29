from smoothsource import smoothsource
from model.model import Model
from model.modelloader import ModelLoader
from model.javamodelcompiler import JavaModelCompiler
from model.cppmodelcompiler import CppModelCompiler
from model.tsmodelcompiler import TypescriptModelCompiler
import getopt
import sys
import traceback

def translatejava(modelpath, genpath):
    model = Model()
    modelloader = ModelLoader(model, modelpath)
    modelloader.load()
    classtemplate = smoothsource.createTemplate(smoothsource.template.Java.xtUMLClassTemplate)
    selectortemplate = smoothsource.createTemplate(smoothsource.template.Java.xtUMLClassSelectorTemplate)
    modelcompiler = JavaModelCompiler(model, genpath, True, classtemplate, selectortemplate)
    modelcompiler.compileAll(persist=True)
    return True

def translatecpp(modelpath, genpath, packageName):
    model = Model()
    modelloader = ModelLoader(model, modelpath)
    modelloader.load()
    assert(packageName and len(packageName) > 0)
    classhtemplate = smoothsource.createTemplate(smoothsource.template.Cpp.xtUMLClassHTemplate)
    classcpptemplate = smoothsource.createTemplate(smoothsource.template.Cpp.xtUMLClassCppTemplate)
    operationcpptemplate = smoothsource.createTemplate(smoothsource.template.Cpp.xtUMLOperationCppTemplate)
    modelcompiler = CppModelCompiler(model, genpath, True, packageName, classhtemplate, classcpptemplate, operationcpptemplate)
    modelcompiler.compileAll(persist=True)
    return True

def translatets(modelpath, genpath, packageName):
    try:
        model = Model()
        modelloader = ModelLoader(model, modelpath)
        modelloader.load()
        assert(packageName and len(packageName) > 0)
        classtemplate = smoothsource.createTemplate(smoothsource.template.Typescript.xtUMLClassTsTemplate)
        classdtemplate = smoothsource.createTemplate(smoothsource.template.Typescript.xtUMLClassDTsTemplate)
        interfacetemplate = smoothsource.createTemplate(smoothsource.template.Typescript.xtUMLInterfaceTsTemplate)
        modelcompiler = TypescriptModelCompiler(model, genpath, True, packageName, classtemplate, classdtemplate, interfacetemplate)
        modelcompiler.compileAll(persist=True)
        return True
    except Exception:
        print(traceback.format_exc())
    return False

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

    translatecpp(modelpath, genpath, "gen")


if __name__ == "__main__":
    main()