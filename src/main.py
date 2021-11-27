from smoothsource import smoothsource

def main():
    smoothsrc = smoothsource()

    model = smoothsrc.loadModel("test/xtuml")

    mockParams = {
            "packageName": "Package",
            "className": "Foo",
            "attributes": [
                {"attributeType": "Integer", "attributeName": "x"},
                {"attributeType": "Integer", "attributeName": "y"}
            ]
        }
    #smoothsrc.populateTemplate(smoothsource.template.Java.ClassTemplate, mockParams)

    classTemplate = smoothsrc.createTemplate(smoothsource.template.Java.xtUMLClassTemplate)

    modelcompiler = smoothsrc.createModelCompiler(model, classTemplate, "test/xtuml/gen")

    modelcompiler.compileAll(persist=True)


if __name__ == "__main__":
    main()