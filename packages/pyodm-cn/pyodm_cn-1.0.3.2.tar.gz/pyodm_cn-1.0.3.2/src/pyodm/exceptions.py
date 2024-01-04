import enum


class CdiscDefineRequiredException(Exception): ...


class ParserException(Exception): ...


class XmlWriterException(Exception): ...


class CdiscFactoryException(Exception): ...


class ErrCode(enum.Enum):
    NoExist = "Not Exist"


class AttributeException(Exception):
    def __init__(self, attribute: str, clazz: str, err: ErrCode, expect=""):
        self.message = f'{attribute} {err.value} {expect} in {clazz}'

    def __str__(self): return self.message


class ElementException(Exception):
    def __init__(self, element: str, clazz: str, err: ErrCode, expect=""):
        self.message = f'{element} {err.value} {expect} in {clazz}'

    def __str__(self): return self.message
