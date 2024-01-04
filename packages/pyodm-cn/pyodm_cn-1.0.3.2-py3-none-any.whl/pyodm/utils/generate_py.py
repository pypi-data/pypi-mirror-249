import copy
import os

from jinja2 import FileSystemLoader, Environment
from lxml import etree


class GeneratePy:
    def __init__(self, xsd_file):
        self.xsd_file = xsd_file
        self.attributeGroups = dict()
        self.complexTypes = dict()
        self.cdiscElements = dict()
        self.groups = dict()

    def generate(self):
        xsd_tree = etree.parse(self.xsd_file)
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
        self.groups[element.attrib._get("name")] = dict(elements=[])
        for x in element:
            if not isinstance(x.tag, str): continue
            if etree.QName(x.tag).localname == "sequence":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "element":
                        ref = y.attrib._get("ref").replace(":", "_")
                        cls_type = "model.OneElement()" if y.attrib._get("maxOccurs") is None else "model.ManyElements()"
                        self.groups[element.attrib._get("name")]["elements"].append(
                            dict(name=ref, cls_type=cls_type))

    def cdisc_element(self, element):
        self.cdiscElements[element.attrib._get("name")] = element.attrib._get("type")

    def attributeGroup(self, element):
        self.attributeGroups[element.attrib._get("name")] = dict()
        for attribute in element:
            if not isinstance(attribute.tag, str): continue
            if etree.QName(attribute.tag).localname == "attribute":
                name = attribute.attrib._get("name") or attribute.attrib._get("ref").replace(":", "_")
                self.attributeGroups[element.attrib._get("name")].update({
                    name: "model.Attribute()"})

    def complexType(self, element):
        """
        临时的解析代码
        :param element:
        :type element:
        :return:
        :rtype:
        """
        self.complexTypes[element.attrib._get("name")] = dict(elements=[], attributes=[], elementGroup=[])
        for x in element:
            if not isinstance(x.tag, str): continue
            if etree.QName(x.tag).localname == "sequence":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "element":
                        ref = y.attrib._get("ref").replace(":", "_")
                        cls_type = "model.OneElement()" if y.attrib._get("maxOccurs") is None else "model.ManyElements()"
                        self.complexTypes[element.attrib._get("name")]["elements"].append(dict(name=ref, cls_type=cls_type))
                    if etree.QName(y.tag).localname == "group":
                        ref = y.attrib._get("ref").replace(":", "_")
                        self.complexTypes[element.attrib._get("name")]["elementGroup"].append(ref)
            if etree.QName(x.tag).localname == "attributeGroup":
                self.complexTypes[element.attrib._get("name")]["attributes"].append(x.attrib._get("ref").replace(":", "_"))
            if etree.QName(x.tag).localname == "simpleContent":
                for y in x:
                    if not isinstance(y.tag, str): continue
                    if etree.QName(y.tag).localname == "extension":
                        for z in y:
                            if not isinstance(z.tag, str): continue
                            if etree.QName(z.tag).localname == "attributeGroup":
                                if not isinstance(z.tag, str): continue
                                self.complexTypes[element.attrib._get("name")]["attributes"].append(
                                            z.attrib._get("ref").replace(":", "_"))


    def console(self):
        print(self.cdisc())
        # print(self.attributeGroups)
        # print(self.cdiscElements)
        # print(self.complexTypes)

    def cdisc(self):
        results = {}
        for name, complex_type in self.cdiscElements.items():
            results[name] = {"elements": copy.deepcopy(self.complexTypes[complex_type]._get("elements")), "attributes": {}}
            for groupName in self.complexTypes[complex_type]._get("elementGroup"):
                if self.groups.get(groupName) is None: continue
                for element in self.groups[groupName]._get("elements"):
                    results[name]["elements"].append(element)
            for ref in self.complexTypes[complex_type]._get("attributes"):
                attrib = self.attributeGroups.get(ref)
                if attrib is not None:
                    results[name]["attributes"].update(attrib)
        return results

    def write_spec(self, cdiscs):
        file_loader = FileSystemLoader('./')
        env = Environment(loader=file_loader)
        template = env.get_template("template/spec.template")
        output = template.render(cdiscs=cdiscs)
        if not os.path.exists('out_put'): os.mkdir('out_put')
        with open(os.path.join('out_put', 'spec.py'), "w", encoding="UTF-8") as f:
            f.write(output)

    def write_cdisc(self, cdiscs):
        file_loader = FileSystemLoader('./')
        env = Environment(loader=file_loader)
        template = env.get_template("template/cdsic.template")

        if not os.path.exists('out_put'): os.mkdir('out_put')
        for cdiscName, cdisc in cdiscs.items():
            output = template.render(cdiscName=cdiscName, cdisc=cdisc)
            with open(os.path.join('out_put', f'{cdiscName}.py'), "w", encoding="UTF-8") as f:
                f.write(output)

if __name__ == '__main__':
    f = "D:\\github\\pyodm\\src\\pyodm\\resources\odm\\schema\\ODM-protocol.xsd"
    g = GeneratePy(f)
    g.generate()
    g.write_spec(g.cdisc())
    g.write_cdisc(g.cdisc())

