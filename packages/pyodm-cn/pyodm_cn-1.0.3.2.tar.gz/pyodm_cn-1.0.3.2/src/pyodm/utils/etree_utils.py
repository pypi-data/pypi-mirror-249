from lxml import etree
from lxml.etree import Element

from pyodm.exceptions import AttributeException, ErrCode


class EtreeUtils:
    @staticmethod
    def localname(element):
        return etree.QName(element.tag).localname

    @staticmethod
    def attrib(element: Element, attrib_name, strict=False):
        value = element.attrib.get(attrib_name)
        if not strict: return value
        if value is None: raise AttributeException(attrib_name, EtreeUtils.localname(element), ErrCode.NoExist)
        return value
