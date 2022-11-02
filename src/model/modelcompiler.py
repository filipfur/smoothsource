import os
import shutil

class ModelCompiler:
    def __init__(self, model, genpath):
        self.model = model
        self.genpath = genpath
        self.createdir(genpath)

    def rmdir(self, dirpath):
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

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