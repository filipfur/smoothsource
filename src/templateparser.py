class TemplateParser:

    def __init__(self, templatepath):
        self.content = None
        with open(templatepath, 'r') as f:
            self.content = f.read()

    def upperCC(self, text):
        return text.capitalize()

    def expandParameter(self, parameter, parameterMap):
        arr = parameter.split(":")
        if len(arr) > 1:
            return self.__getattribute__(arr[1])(parameterMap[arr[0]])
        else:
            return parameterMap[parameter]

    def parseParameters(self, content, parameterMap):
        start = content.find("{{")
        while start != -1:
            start += 2
            end = content.find("}}", start)
            parameter = content[start:end]
            tmp = content[0:start - 2] + self.expandParameter(parameter, parameterMap) + content[(end + 2):]
            content = tmp
            start = content.find("{{")
        return content


    def parseArrays(self, content):
        start = content.find("[[")
        while start != -1:
            indentation = 64
            for i in range(64):
                if content[start - 1 - i] != ' ':
                    indentation = i
                    break
            #delim = "\n" + ' ' * indentation
            start += 2
            end = content.find("]]", start)
            subcontent = content[start:end]
            arrayName = subcontent[0:subcontent.find("|")]
            subcontent = subcontent[(subcontent.find("|") + 1):]
            arrayContent = ""
            for parameterMap in self.parameters[arrayName]:
                arrayContent += self.parseParameters(subcontent, parameterMap) #+ delim
            tmp = content[0:start - 2] + arrayContent + content[(end + 2):]
            content = tmp
            start = content.find("[[")
        return content


    def parse(self):
        self.parameters = {
            "packageName": "Package",
            "className": "Foo",
            "attributes": [
                {"attributeType": "Integer", "attributeName": "x"},
                {"attributeType": "Integer", "attributeName": "y"}
            ]
        }
        content = self.parseArrays(self.content)
        content = self.parseParameters(content, self.parameters)
        print("output:")
        print(content)