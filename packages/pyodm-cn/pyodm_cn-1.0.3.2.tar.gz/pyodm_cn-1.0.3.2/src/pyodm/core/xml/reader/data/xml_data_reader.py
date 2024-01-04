from lxml import etree

from pyodm.core.support.abstract_data_loader import AbstractDataLoader
from pyodm.core.support.abstract_data_reader import AbstractDataReader
from pyodm.factory.cdisc_registry import CdiscRegistry
from pyodm.model.definition import OneElement, ManyElements
from pyodm.utils.etree_utils import EtreeUtils


class XMLDataReader(AbstractDataReader):
    """
    读取 XML 文件的实现
    """

    def __init__(self, registry: CdiscRegistry):
        super().__init__(registry)

    def _new_cdisc_node(self, cdisc_name):
        new_obj = self.registry.get(cdisc_name)()
        return new_obj

    def _set_attribute(self, element, cdisc_node):
        for key, val in element.attrib.items():
            attr = getattr(cdisc_node, key)
            attr.set_name(key)
            attr.set_value(val)

    def _sub_cdisc_node(self, cdisc_node, sub_cdisc_name):
        return getattr(cdisc_node, sub_cdisc_name)

    def _set_text(self, element, cdisc_node):
        if element.text and not element.text.isspace() and element.text.strip():
            cdisc_node.set_value(element.text)

    def _parse(self, element, cdisc_name):
        cdisc_node = self._new_cdisc_node(cdisc_name)
        cdisc_node.set_name(cdisc_name)
        # 处理属性节点
        self._set_attribute(element, cdisc_node)
        # 处理文本节点
        self._set_text(element, cdisc_node)
        for sub_element in element:
            if isinstance(sub_element, etree._Comment): continue  # 忽略注释
            sub_cdisc_name = EtreeUtils.localname(sub_element)
            # 获取 子节点 实例
            sub_cdisc_node = self._sub_cdisc_node(cdisc_node, sub_cdisc_name)
            # 处理类型为 OneElement的Element的对象
            self._one_element(cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name)
            # 处理类型为 ManyElements的Element的对象
            self._many_element(cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name)
        return cdisc_node

    def _many_element(self, cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name):
        if isinstance(sub_cdisc_node, ManyElements):
            many_element = sub_cdisc_node
            many_element.set_name(sub_cdisc_name)
            many_element << self._parse(sub_element, sub_cdisc_name)

    def _one_element(self, cdisc_node, sub_cdisc_node, sub_element, sub_cdisc_name):
        if isinstance(sub_cdisc_node, OneElement):
            one_element = self._parse(sub_element, sub_cdisc_name)
            one_element.set_name(sub_cdisc_name)
            setattr(cdisc_node, sub_cdisc_name, one_element)

    def read(self, loader: AbstractDataLoader):
        tree = loader.load()
        return self._parse(tree.getroot(), EtreeUtils.localname(tree.getroot()))
