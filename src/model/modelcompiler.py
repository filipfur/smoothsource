import os
import shutil

class ModelCompiler:
    def __init__(self, model, genpath, removeOld):
        self.model = model
        self.genpath = genpath
        if removeOld:
            self.clearGenPath()
        self.createdir(genpath)

    def clearGenPath(self):
        if os.path.isdir(self.genpath):
            shutil.rmtree(self.genpath)

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