import copy

from lxml import etree

from pyodm.core.support.abstract_configuration_reader import AbstractConfigurationReader
import pyodm.model.definition as Model
from pyodm.factory.cdisc_registry import CdiscRegistry
from pyodm.factory.xpath.xpath_node import XpathNode
from pyodm.model.meta.cdisc_odm_entity import CdiscODMEntity


# TODO 变量的域的区分 xmlns(基本功能完成后再做)
class CdiscConfigurationXsdReader(AbstractConfigurationReader):
    """
    读取 ODM XSD 格式的配置文件
    https://github.com/cdisc-org/DataExchange-ODM/tree/main/schema
    """
    def __init__(self):
        self.attributeGroups = dict()
        self.complexTypes = dict()
        self.cdiscElements = dict()
        self.groups = dict()

    def load(self, xsd_file):
        xsd_tree = etree.parse(xsd_file)
        root = xsd_tree.getroot()
        for element in root:
            if not isinstance(element.tag, str): continue
            name = etree.QName(element.tag).localname
            if name == "attributeGroup":
                self.attributeGroup(element)
            if name == "complexType":
                self.complexType(element)
            if name == "element":
                self.cdisc_element(element)
            if name == 'group':
                self.group(element)
            # print(element)

    def group(self, element):
        self.groups[element.attrib.get("name")] = dict(elements=[])
        for x in element:
            if not isinstance(x.tag, str): continue
            if etree.QName(x.tag).localname == "sequence":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "element":
                        ref = y.attrib.get("ref").replace(":", "_")
                        cls_type = "model.OneElement()" if y.attrib.get("maxOccurs") is None else "model.ManyElements()"
                        self.groups[element.attrib.get("name")]["elements"].append(
                            dict(name=ref, cls_type=cls_type))

    def cdisc_element(self, element):
        self.cdiscElements[element.attrib.get("name")] = element.attrib.get("type")

    def attributeGroup(self, element):
        self.attributeGroups[element.attrib.get("name")] = dict()
        for attribute in element:
            if not isinstance(attribute.tag, str): continue
            if etree.QName(attribute.tag).localname == "attribute":
                name = attribute.attrib.get("name") or attribute.attrib.get("ref").replace(":", "_")
                self.attributeGroups[element.attrib.get("name")].update({
                    name: "model.Attribute()"})

    def complexType(self, element):
        """
        临时的解析代码
        :param element:
        :type element:
        :return:
        :rtype:
        """
        self.complexTypes[element.attrib.get("name")] = dict(elements=[], attributes=[], elementGroup=[])
        for x in element:
            if not isinstance(x.tag, str): continue
            if etree.QName(x.tag).localname == "sequence":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "element":
                        ref = y.attrib.get("ref").replace(":", "_")
                        cls_type = "model.OneElement()" if y.attrib.get("maxOccurs") is None else "model.ManyElements()"
                        self.complexTypes[element.attrib.get("name")]["elements"].append(
                            dict(name=ref, cls_type=cls_type))
                    if etree.QName(y.tag).localname == "group":
                        ref = y.attrib.get("ref").replace(":", "_")
                        self.complexTypes[element.attrib.get("name")]["elementGroup"].append(ref)
            if etree.QName(x.tag).localname == "attributeGroup":
                self.complexTypes[element.attrib.get("name")]["attributes"].append(
                    x.attrib.get("ref").replace(":", "_"))
            if etree.QName(x.tag).localname == "simpleContent":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "extension":
                        for z in y:
                            if not isinstance(z.tag, str): continue
                            if etree.QName(z.tag).localname == "attributeGroup":
                                if not isinstance(z.tag, str): continue
                                self.complexTypes[element.attrib.get("name")]["attributes"].append(
                                    z.attrib.get("ref").replace(":", "_"))

    def cdisc(self):
        results = {}
        for name, complex_type in self.cdiscElements.items():
            results[name] = {"elements": copy.deepcopy(self.complexTypes[complex_type].get("elements")),
                             "attributes": {}}
            for groupName in self.complexTypes[complex_type].get("elementGroup"):
                if self.groups.get(groupName) is None: continue
                for element in self.groups[groupName].get("elements"):
                    results[name]["elements"].append(element)
            for ref in self.complexTypes[complex_type].get("attributes"):
                attrib = self.attributeGroups.get(ref)
                if attrib is not None:
                    results[name]["attributes"].update(attrib)
        return results

    def load_cdisc_definition(self, registry: CdiscRegistry, xsd_files: list):
        for xsd_file in xsd_files:
            self.load(xsd_file=xsd_file)
        for name, clazz_info in self.cdisc().items():
            registry.registry_cdisc(name=name, cdisc_class=self._clazz_parser(name, clazz_info, registry))

    def _clazz_parser(self, name, clazz_info: dict, registry: CdiscRegistry):
        __definition = {
            "model.Attribute()": Model.Attribute,
            "model.OneElement()": Model.OneElement,
            "model.ManyElements()": Model.ManyElements
        }
        attrs = {}
        for element in clazz_info.get("elements"):
            cdisc_definition = __definition.get(element.get("cls_type"))()
            cdisc_definition.parent = name
            attrs[element.get("name")] = cdisc_definition
        for attribute_name, cls_type in clazz_info.get("attributes").items():
            attrs[attribute_name] = __definition.get(cls_type)()
        registry.definition_tree.add(XpathNode(name), [XpathNode(e.get('name')) for e in clazz_info.get("elements")])
        return type(name, (CdiscODMEntity,), attrs)

