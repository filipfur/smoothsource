from os import system
from template.fragment import Fragment
from template.text import Text
from template.parameter import Parameter

class Segment(Fragment):

    def __init__(self, content, root=False):
        self._fragments = []
        self._name = ""
        self._root = root
        if not root:
            pipeIndex = content.find("|")
            self._name = content[0:pipeIndex]
            content = content[pipeIndex + 1:]
        self._content = content
        done = False
        i = 0
        while i < len(content) and not done:
            arrayStart = content.find("[[", i)
            paramStart = content.find("{{", i)
            if paramStart == -1 and arrayStart == -1:
                self._fragments.append(Text(content[i:]))
                done = True
            elif paramStart == -1 or (arrayStart != -1 and arrayStart < paramStart):
                if i < arrayStart:
                    self._fragments.append(Text(content[i:arrayStart]))
                arrayEnd = content.find("]]", arrayStart + 2)
                self._fragments.append(Segment(content[arrayStart + 2:arrayEnd])) #TODO: handle nested arrays
                i = arrayEnd + 2
            else:
                if i < paramStart:
                    self._fragments.append(Text(content[i:paramStart]))
                paramEnd = content.find("}}", paramStart + 2)
                self._fragments.append(Parameter(content[paramStart + 2:paramEnd]))
                i = paramEnd + 2

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
            for ad in arrayData:
                data.append(ad)
                text = self.populateFragments(data, scope)
                data.pop()
        if text == "":
            print("Empty frag: %s" % self._name)
        return text
        

    def __str__(self):
        text = "Segment(_name=%s)" % self._name + "\n"
        for fragment in self._fragments:
            text += str(fragment) + "\n"
        return text

    def name(self):
        return self._name