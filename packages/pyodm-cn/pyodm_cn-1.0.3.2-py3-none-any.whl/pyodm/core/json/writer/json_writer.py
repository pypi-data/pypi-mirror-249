import json
from pathlib import Path
import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta
from pyodm.core.xml.writer.write_status import WriteStatus
from pyodm.exceptions import XmlWriterException


def cdisc(model):
    def __inner__(func):
        def __wrapper__(self, cdisc, element):
            if isinstance(cdisc, model):
                status = func(self, cdisc, element)
                if status == WriteStatus.IGNORE: return WriteStatus.IGNORE
            else:
                return WriteStatus.PASS
            return WriteStatus.OK

        return __wrapper__

    return __inner__


class JSONWriter:
    def __init__(self, out_put: Path, data):
        self.out_put = out_put
        self._data = data

    def write(self):
        if not isinstance(self._data, Meta.CdiscODMEntity):
            raise XmlWriterException("data should instance of CdiscODMEntity")
        json_data = dict()

        for action in [self._entity, self._many_element, self._one_element]:
            status = action(self._data, json_data)
            if status != WriteStatus.PASS: break
        print(json_data)
        with open(self.out_put, 'w') as f:
            f.write(json.dumps(json_data, indent=4))
        # dump_tree.write(self.out_put, pretty_print=True, encoding="utf-8")

    def is_valid(self, unknown) -> bool:
        return isinstance(unknown, Meta.CdiscODMEntity) or \
               isinstance(unknown, Model.Attribute) or \
               isinstance(unknown, Model.OneElement) or \
               isinstance(unknown, Model.ManyElements)

    @cdisc(model=Meta.CdiscODMEntity)
    def _entity(self, entity, json_data: dict = None) -> WriteStatus:
        for name, entity_instance in vars(entity).items():
            if not self.is_valid(entity_instance): continue
            self._vars_entity(entity_instance, json_data=json_data)

    @cdisc(model=Model.Attribute)
    def _attribute(self, entity: Model.Attribute, json_data: dict = None):
        if entity.no_use(): return WriteStatus.IGNORE
        # json_data[entity.get_name()] = str(entity.get_value())
        json_data[entity.get_name()] = entity.get_value()

    @cdisc(model=Model.OneElement)
    def _one_element(self, entity: Model.OneElement, json_data: dict = None) -> WriteStatus:
        if entity.no_use(): return WriteStatus.IGNORE
        if not json_data.get(entity.get_name()): json_data[entity.get_name()] = dict
        for name, cdisc_instance in vars(cdisc).items():
            if not self.is_valid(cdisc_instance): continue
            # if not entity.is_blank(): element.text = cdisc.value
            self._vars_entity(cdisc_instance, json_data.get(entity.get_name()))

    @cdisc(model=Model.ManyElements)
    def _many_element(self, entity: Model.ManyElements, json_data: dict = None) -> WriteStatus:
        if entity.no_use(): return WriteStatus.IGNORE
        if not json_data.get(entity.get_name()): json_data[entity.get_name()] = list()
        for e in entity.array:
            object_data = dict()
            self._entity(e, object_data)
            json_data.get(entity.get_name()).append(object_data)

    def _vars_entity(self, entity, json_data: dict = None):
        for action in [self._attribute, self._many_element, self._one_element]:
            status = action(entity, json_data)
            if status != WriteStatus.PASS: break
        if status == WriteStatus.PASS:
            self._entity(entity, json_data.get(entity.get_name(), dict()))
