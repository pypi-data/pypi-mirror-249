class Finder:
    def __init__(self):
        self._element_name = None
        self._attribute = dict()
        self._text = None

    def element(self, name: str):
        self._element_name = name
        return self

    def attribute(self, **kwargs):
        self._attribute.update(kwargs)
        return self

    def text(self, value):
        self._text = value
        return self

    def _attribute_match(self, element):
        for key, value in self._attribute.items():
            if element.__dict__.get(key) is None: return False
            if element.__dict__.get(key).get_value() != value: return False
        return True

    def _text_match(self, element):
        if self._text is None: return True
        else: return element.get_value() == self._text

    def _name_match(self, element):
        return element.get_name() == self._element_name

    def Lambda(self):
        return lambda x: self._name_match(x) and self._attribute_match(x) and self._text_match(x)
