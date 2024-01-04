import pyodm.model.definition as Model
# from pyodm.core.parser import Parser


class EntityMeta(type):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Model.Attribute):
                attr.set_name(key)
            if isinstance(attr, Model.OneElement):
                attr.set_name(key)
            if isinstance(attr, Model.ManyElements):
                attr.set_name(key)

