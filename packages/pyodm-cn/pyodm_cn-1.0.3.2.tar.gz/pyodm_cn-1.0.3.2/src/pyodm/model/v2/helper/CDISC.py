from typing import Type


class Mixin:

    @classmethod
    def first(cls): return cls

    @classmethod
    def find(cls, **attributes): return cls

    @classmethod
    def index(cls, i): return cls

    @classmethod
    def array(cls): return [cls]

    @property
    def name(self): ...

    @property
    def value(self): ...


class Attribute:
    @property
    def name(self): ...

    @property
    def value(self): ...


class Model:
    @staticmethod
    def Attribute() -> Attribute: ...

    @staticmethod
    def OneElement() -> Mixin: ...


class SignatureRef(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/SignatureRef+Element
    """

    SignatureOID = Model.Attribute()


class Signature(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/Signature+Element
    """
    SignatureRef: SignatureRef = Model.OneElement()


class ClinicalData(Mixin):
    """
    https://wiki.cdisc.org/display/ODM2/ClinicalData+Element
    """

    Signature: Signature = Model.OneElement()
