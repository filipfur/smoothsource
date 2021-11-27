from smoothsource import smoothsource

def main():
    model = smoothsource.loadModel("C:\\Users\\Filip Fur\\Desktop\\xtuml_plugin\\xtuml")

    for uid in model.classes():
        print(uid)

    smoothsource.parseTemplate("template\\Class.javat")


if __name__ == "__main__":
    main()