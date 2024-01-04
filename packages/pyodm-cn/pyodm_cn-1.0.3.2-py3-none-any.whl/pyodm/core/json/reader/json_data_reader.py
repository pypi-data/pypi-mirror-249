from pyodm.core.support.abstract_data_loader import AbstractDataLoader
from pyodm.core.support.abstract_data_reader import AbstractDataReader


class JsonDataReader(AbstractDataReader):
    def read_specified(self, specified_name: str, loader: AbstractDataLoader):
        json_data = loader.load()
        return self._parse(json_data, specified_name)

    def read(self, loader: AbstractDataLoader):
        ...

    def _new_node(self, name):
        new_obj = self.registry.get(name)()
        return new_obj

    def _parse(self, data: dict, name):
        cdisc_node = self._new_node(name)
        cdisc_node.set_name(name)
        for key, value in data.items():
            if isinstance(value, dict):
                # One Element
                one_element = self._parse(value, key)
                one_element.set_name(key)
                setattr(cdisc_node, key, one_element)
            elif isinstance(value, list):
                # Many Element
                sub_cdisc_node = getattr(cdisc_node, key)
                sub_cdisc_node.set_name(key)
                for e in value:
                    sub_cdisc_node << self._parse(e, key)
            else:
                # Attribute
                attr = getattr(cdisc_node, key)
                attr.set_name(key)
                attr.set_value(value)
        return cdisc_node
