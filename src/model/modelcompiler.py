import os

class ModelCompiler:
    def __init__(self, model, genpath):
        self.model = model
        self.genpath = genpath
        self.createdir(genpath)

    def create(self, fpath, text, persist):
        print("ModelCompiler::Create: " + fpath)
        if persist:
            with open(fpath, 'w') as f:
                f.write(text)
        else:
            print(text)

    def createdir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def compileAll(self, persist=True):
        pass