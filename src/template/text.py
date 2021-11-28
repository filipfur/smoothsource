from template.fragment import Fragment

class Text(Fragment):

    def __init__(self, text):
        self._text = text

    def populate(self, data, scope):
        return self._text

    def __str__(self):
        return "Text(%s)" % self._text