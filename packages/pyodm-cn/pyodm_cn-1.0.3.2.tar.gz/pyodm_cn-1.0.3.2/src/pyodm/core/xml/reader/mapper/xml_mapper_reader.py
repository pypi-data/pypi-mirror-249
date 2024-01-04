from xml.etree.ElementTree import ElementTree

from cjen.mama.meta_data import MetaData
from lxml.etree import Element

from pyodm.core.support.abstract_data_loader import AbstractDataLoader
from pyodm.core.support.abstract_data_reader import AbstractDataReader
from pyodm.exceptions import AttributeException, ErrCode, ElementException
from pyodm.factory.cdisc_registry import CdiscRegistry
from pyodm.utils.class_utils import ClassUtils
from pyodm.utils.dict_utils import DictUtils
from pyodm.utils.etree_utils import EtreeUtils


class XMLMapperReader(AbstractDataReader):
    ODM_CLASS = "ODMClass"
    TEXT = "Text"

    def __init__(self, registry: CdiscRegistry, data: MetaData):
        super().__init__(registry)
        self._array = []
        self.data = data

    def read(self, resource: AbstractDataLoader):
        tree = self._load(resource)
        self._parse_element(tree.getroot(), level=1)
        return self._array

    def _parse_element(self, element: Element, level: int):
        if len(self._array) < level: self._array.append(dict())
        class_name = EtreeUtils.attrib(element, self.ODM_CLASS, strict=True)
        self._array[level - 1][class_name] = dict()
        attributes = DictUtils.filter(element.attrib, lambda key, value: key != self.ODM_CLASS and key != self.TEXT)
        for attribute_name, field in attributes.items():
            if not self._contain_attribute(attribute_name, class_name):
                raise AttributeException(attribute_name, class_name, ErrCode.NoExist)
            self._array[level - 1][class_name][attribute_name] = self.data.meta_data[field]
        if EtreeUtils.attrib(element, self.TEXT) is not None:
            self._array[level - 1][class_name][self.TEXT] = self.data.meta_data[self.TEXT]
        for sub_element in element.getchildren():
            sub_class_name = EtreeUtils.attrib(sub_element, self.ODM_CLASS, strict=True)
            if not self._contain_elements(sub_class_name, class_name):
                raise ElementException(sub_class_name, class_name, ErrCode.NoExist)
            self._parse_element(sub_element, level + 1)

    def _contain_attribute(self, attribute_name, class_name) -> bool:
        return attribute_name in ClassUtils.attributes_name(clazz=self.registry.get(class_name))

    def _contain_elements(self, element_name, class_name) -> bool:
        return element_name in ClassUtils.elements_name(clazz=self.registry.get(class_name))

    def _load(self, loader: AbstractDataLoader) -> ElementTree:
        return loader.load()
