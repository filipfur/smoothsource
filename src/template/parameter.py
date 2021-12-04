from template.fragment import Fragment
import datetime

class Parameter(Fragment):

    def __init__(self, name):
        arr = name.split(":")
        self._name = arr[0]
        self._operands = []
        for op in arr[1:]:
            self._operands.append(self.__getattribute__("_" + op))

    # TODO: add :datetime@format@
    def _datetime(self, text):
        return str(datetime.datetime.now())

    def _upperCC(self, text):
        return text[0].upper() + text[1:]

    def _lowerCC(self, text):
        return text[0].lower() + text[1:]

    def _variable(self, text):
        return self._lowerCC(text)

    def _class(self, text):
        return self._upperCC(text)

    def transform(self, text):
        for op in self._operands:
            text = op(text)
        return text

    def populate(self, data, scope):
        text = ""
        while len(text) == 0 and scope >= 0:
            if self._name in data[scope]:
                text = self.transform(str(data[scope][self._name]))
            elif len(self._operands) > 0:
                text = self.transform("")
            scope -= 1
        return text

    def name(self):
        return self._name


    def __str__(self):
        return "Parameter(_name=%s)" % self._name