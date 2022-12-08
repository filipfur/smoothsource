from os import system
from template.fragment import Fragment
from template.text import Text
from template.parameter import Parameter

class Container:

    Max = 1000000

    def __init__(self, startToken, start):
        self._startToken = startToken
        self._start = start
        if self._start == -1:
            self._start = Container.Max

class Segment(Fragment):

    def __init__(self, content, root=False, delim="", iscond=False):
        self._fragments = []
        self._name = ""
        self._root = root
        self._iscond = iscond
        self._delim = delim
        self._begin = ""
        self._end = ""
        if not root:
            pipeIndex = content.find("|")
            self._name = content[0:pipeIndex]
            self.expandName()
            content = content[pipeIndex + 1:]
        self._content = content
        done = False
        i = 0
        while i < len(content) and not done:
            arrayStart = content.find("[[", i)
            paramStart = content.find("{{", i)
            condStart = content.find("<?", i)

            containers = sorted([Container("[[", arrayStart), Container("{{", paramStart), Container("<?", condStart)], key=lambda x: x._start)

            container = containers[0]

            if container._start == Container.Max:
                self._fragments.append(Text(content[i:]))
                done = True
            elif container._startToken == "<?":
                lastNewLine = content.rfind("\n", 0, condStart)
                if i < condStart:
                    text = content[i:lastNewLine]
                    self._fragments.append(Text(text))
                
                delim = ""
                for i in range(1, condStart):
                    c = content[condStart - i]
                    if c == " " or c == "\n":
                        delim = c + delim
                    else:
                        break

                arrayEnd = content.find("?>", condStart + 2)
                self._fragments.append(Segment(content[condStart + 2:arrayEnd], delim=delim, iscond=True)) #TODO: handle nested conditions
                i = arrayEnd + 2
            elif container._startToken == "[[":
                lastNewLine = content.rfind("\n", 0, arrayStart)
                if i < arrayStart:
                    self._fragments.append(Text(content[i:lastNewLine]))
                
                delim = ""
                for i in range(1, arrayStart):
                    c = content[arrayStart - i]
                    if c == " " or c == "\n":
                        delim = c + delim
                    else:
                        break

                arrayEnd = content.find("]]", arrayStart + 2)
                self._fragments.append(Segment(content[arrayStart + 2:arrayEnd], delim=delim)) #TODO: handle nested arrays
                i = arrayEnd + 2
            elif container._startToken == "{{":
                if i < paramStart:
                    self._fragments.append(Text(content[i:paramStart]))
                paramEnd = content.find("}}", paramStart + 2)
                indentation = ""
                j = paramStart - 1
                while j >= 0 and (content[j] == " " or content[j] == "\t"):
                    indentation = content[j] + indentation
                    j -= 1
                self._fragments.append(Parameter(content[paramStart + 2:paramEnd], indentation))
                i = paramEnd + 2


    def begin(self, text):
        self._begin = text

    def end(self, text):
        self._end = text

    def expandName(self):
        if ":" in self._name:
            startExtra = self._name.find(":")
            extra = self._name[startExtra:]
            self._name = self._name[0:startExtra]
            done = False
            i = 0
            while not done:
                startExtra = extra.find(":", i)
                if startExtra == -1: # -1
                    done = True
                else:
                    startExtra2 = extra.find(":", startExtra + 1)
                    startParam2 = extra.find("@", startExtra + 1)
                    startExtra2 = 1000000 if startExtra2 == -1 else startExtra2
                    startParam2 = 1000000 if startParam2 == -1 else startParam2
                    if startParam2 == startExtra2: # -1
                        done = True
                        opName = extra[startExtra+1:]
                        self.__getattribute__(opName)()
                    elif startExtra2 < startParam2 and startExtra2:
                        opName = extra[startExtra+1:startExtra2]
                        self.__getattribute__(opName)()
                        i = startExtra2
                    elif startParam2 < startExtra2:
                        opName = extra[startExtra+1:startParam2]
                        endParam = extra.find("@", startParam2 + 1)
                        opParam = extra[startParam2+1:endParam]
                        self.__getattribute__(opName)(opParam)
                        i = endParam + 1

    def populateFragments(self, data, scope):
        text = ""
        for fragment in self._fragments:
            text += fragment.populate(data, scope)
        return text

    def populate(self, data, scope):
        text = ""
        if self._root:
            text = self.populateFragments(data, scope)
        else:
            if self._name not in data[scope]:
                print("Error: '%s' not in data (scope: %d)." % (self._name, scope)) #TODO: handle nested arrays
                exit(1)
            arrayData = data[scope][self._name]
            scope += 1
            delim = self._delim
            begin = self._begin
            end = self._end
            if self._iscond:
                if arrayData == None:
                    arrayData = []
                elif type(arrayData) == bool:
                    if arrayData:
                        arrayData = [{}]
                    else:
                        arrayData = []
                elif type(arrayData) == str:
                    if len(arrayData) == 0:
                        arrayData = []
                    else:
                        arrayData = [{self._name: arrayData}]
            for i, ad in enumerate(arrayData):
                data.append(ad)
                text += delim + begin + self.populateFragments(data, scope)
                if i == len(arrayData) - 1:
                    text += end
                begin = ""
                data.pop()
                if self._iscond:
                    break
        return text
        

    def __str__(self):
        text = "Segment(_name=%s)" % self._name + "\n"
        for fragment in self._fragments:
            text += str(fragment) + "\n"
        return text

    def name(self):
        return self._name