from pyodm.model.meta.entity_meta import EntityMeta
import pyodm.model.definition as Model
#


class CdiscODMEntity(metaclass=EntityMeta):
    """
    自定义ODM的元素的时候，必须继承的元类
    """
    def __init__(self):
        self._name = ""
        self._value = None
        for name, instance in vars(self.__class__).items():
            if isinstance(instance, Model.Attribute) \
                    or isinstance(instance, Model.OneElement) \
                    or isinstance(instance, Model.ManyElements):
                setattr(self, name, instance.__class__())

    def get_name(self):
        return self._name

    def get_value(self): return self._value

    def set_value(self, value): self._value = value

    def set_name(self, value):
        self._name = value

    def is_blank(self) -> bool: return self.get_value() is None

    def as_stream(self):
        from pyodm.utils.stream import Stream
        return Stream(self)
