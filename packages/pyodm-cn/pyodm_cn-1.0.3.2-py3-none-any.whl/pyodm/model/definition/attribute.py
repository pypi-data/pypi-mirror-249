from pyodm.model.definition.cdisc_model import CdiscModel


class Attribute(CdiscModel):
    """
    ODM 标准中对应的 Element 的 Attribute属性
    """

    def __init__(self):
        super().__init__()
        self._value = ""

    def get_name(self): return self._name

    def set_name(self, name): self._name = name

    def get_value(self): return self._value

    def set_value(self, value): self._value = value
