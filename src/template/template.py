from template.segment import Segment

TemplateDir = "template"

class Java:
    JavaDir = TemplateDir + "/java"
    ClassTemplate = JavaDir + "/Class.template"
    xtUMLClassTemplate = JavaDir + "/Class.xtuml.template"

class Template:

    def __init__(self, templatepath):
        self.content = None
        self.templatepath = templatepath
        with open(templatepath, 'r') as f:
            self.content = f.read()
        self.segment = Segment(self.content, root=True)
        print(str(self.segment))



    def upperCC(self, text): # TODO: rename to :class ?
        return text.capitalize()

    def lowerCC(self, text): # TODO: rename to :variable ?
        return text[0].lower() + text[1:]

    def expandParameter(self, parameter, parameterMap):
        arr = parameter.split(":")
        pName = arr[0]
        textContent = None
        if pName in parameterMap:
            textContent = str(parameterMap[pName])
        else:
            textContent = str(self.parameters[pName])
        if len(arr) > 1:
            return self.__getattribute__(arr[1])(textContent)
        else:
            return textContent

    def populateParameters(self, content, parameterMap):
        start = content.find("{{")
        while start != -1:
            start += 2
            end = content.find("}}", start)
            parameter = content[start:end]
            try:
                tmp = content[0:start - 2] + self.expandParameter(parameter, parameterMap) + content[(end + 2):]
            except KeyError as e:
                print("Error when expanding parameter '%s' in template: %s:0" % (parameter, self.templatepath))
                raise(e)
            content = tmp
            start = content.find("{{")
        return content


    def populateArrays(self, content, parameters):
        start = content.find("[[")
        while start != -1:
            start += 2
            end = content.find("]]", start)
            subcontent = content[start:end]
            arrayName = subcontent[0:subcontent.find("|")]
            subcontent = subcontent[(subcontent.find("|") + 1):]
            arrayContent = ""
            if "@" in arrayName:
                arr = arrayName.split("@")
                arrayName = arr[0]
                if len(parameters[arrayName]) > 0:
                    arrayContent += arr[1]
            for parameterMap in parameters[arrayName]:
                arrayContent += self.populateParameters(subcontent, parameterMap)
            if len(arrayContent) == 0:
                skipA = 0
                for i in range(64):
                    c = content[start - 2 - i]
                    if c != ' ' and c != '\n':
                        skipA = i
                        break
                skipB = 0
                for i in range(64):
                    c = content[end + 2 + i]
                    if c != ' ':
                        skipB = i
                        if c == '\n':
                            skipB += 1
                        break
                content = content[0:start - 2 - skipA] + content[(end + 2 + skipB):]
            else:
                content = content[0:start - 2] + arrayContent + content[(end + 2):]
            start = content.find("[[")
        return content


    def templify(self, parameters):
        self.parameters = parameters
        #content = self.populateArrays(self.content, self.parameters)
        #content = self.populateParameters(content, self.parameters)
        content = self.segment.populate([parameters], 0)
        return content