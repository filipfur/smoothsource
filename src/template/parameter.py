from template.fragment import Fragment

class Parameter(Fragment):

    def __init__(self, name):
        arr = name.split(":")
        self._name = arr[0]
        self._operands = []
        for op in arr[1:]:
            self._operands.append(self.__getattribute__(op))

    def upperCC(self, text): # TODO: rename to :class ?
        return text[0].upper() + text[1:]

    def lowerCC(self, text): # TODO: rename to :variable ?
        return text[0].lower() + text[1:]

    def transform(self, text):
        for op in self._operands:
            text = op(text)
        return text

    def populate(self, data, scope):
        text = None
        while text is None and scope >= 0:
            if self._name in data[scope]:
                text = self.transform(str(data[scope][self._name]))
            scope -= 1
        return text

    def name(self):
        return self._name


    def __str__(self):
        return "Parameter(_name=%s)" % self._name