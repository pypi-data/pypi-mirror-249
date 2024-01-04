from pyodm.core.data_loader.forest_data_loader import ForestDataLoader
from pyodm.core.support.abstract_data_reader import AbstractDataReader
from pyodm.factory.cdisc_registry import CdiscRegistry
from pyodm.model.definition import ManyElements, OneElement, Attribute
from pyodm.model.meta.cdisc_odm_entity import CdiscODMEntity
from pyodm.utils.forest import Forest


class ForestDataReader(AbstractDataReader):
    """
    读取Forest类型数据，把 Forest 类型转化为 ODM 数据
    """

    def __init__(self, registry: CdiscRegistry):
        super().__init__(registry)

    def read(self, data_loader: ForestDataLoader):
        forest_data = data_loader.load()
        result = self.read_data(forest_data)
        if len(result) == 1: return result[0]
        return result

    def read_data(self, forest_data: Forest):
        # self.otree = otree
        result = []
        for node in forest_data.get_level_nodes(0):
            for node_name, node_value in node.values.items():
                result.append(self._scan(node, node_name, node_value))
        return result

    def _sub_cdisc_node(self, cdisc_node, sub_cdisc_name):
        return getattr(cdisc_node, sub_cdisc_name)

    def _new_cdisc_node(self, cdisc_name):
        new_obj = self.registry.get(cdisc_name)()
        new_obj.set_name(cdisc_name)
        return new_obj

    def _scan(self, node, cdisc_name, node_value):
        cdisc = self._new_cdisc_node(cdisc_name)
        for key, value in node_value.items():
            if key == "Text":
                cdisc.set_value(value)
            else:
                attribute = getattr(cdisc, key)
                if attribute is None: raise Exception(f'{cdisc.get_name} have not attribute {key}')
                if not isinstance(attribute, Attribute): raise Exception(f'{cdisc.get_name} {key} is not Attribute')
                attribute.set_name(key)
                attribute.set_value(value)

        for sub_node in node.children():
            for sub_node_name, sub_node_value in sub_node.values.items():
                element = getattr(cdisc, sub_node_name, None)
                # if element is None: raise Exception(f'{cdisc.name} have not element {sub_node_name}')
                if element is None: continue
                if not isinstance(element, OneElement) and not isinstance(element, ManyElements) \
                        and not isinstance(element, CdiscODMEntity):
                    raise Exception(f'{cdisc.get_name()} {sub_node_name} is not element')
                if isinstance(element, OneElement):
                    setattr(cdisc, sub_node_name, self._scan(sub_node, sub_node_name, sub_node_value))
                elif isinstance(element, ManyElements):
                    element.set_name(sub_node_name)
                    element << self._scan(sub_node, sub_node_name, sub_node_value)
        return cdisc

    def _parse(self, cdisc, node_value: dict, otree_index=0):
        for attr_name, attr_obj in vars(cdisc).items():
            if node_value.get(attr_name) is not None:
                attr_obj.set_name(attr_name)
                attr_obj.set_value(node_value.get(attr_name))
        if node_value.get("Text") is not None:
            cdisc.set_value(node_value.get("Text"))
        self._scan(cdisc.get_name(), otree_index)
        return cdisc

    def _set_text(self, node_name, attr_name, info_dict, cdisc_node):
        if node_name == attr_name:
            if info_dict.get("Text") is not None:
                cdisc_node.set_value(info_dict.get("Text"))
                return True
        return False

    def _set_attribute(self, node_name, attr_name, node, cdisc_node):
        if node_name == attr_name:
            for name, attr_obj in vars(cdisc_node).items():
                if node.get(name) is not None:
                    attr_obj.set_name(name)
                    attr_obj.set_value(node.values.get(name))

    def _many_element(self, node_name, attr_name, sub_cdisc_node, otree_index):
        if isinstance(sub_cdisc_node, ManyElements):
            sub_cdisc_node << self._parse(self.registry.get(sub_cdisc_node.get_name()), otree_index)

    def _one_element(self, node_name, attr_name, sub_cdisc_node, otree_index):
        if isinstance(sub_cdisc_node, OneElement):
            self._parse(self.registry.get(sub_cdisc_node.get_name()), otree_index)

