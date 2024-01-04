
from pyodm.core.support.abstract_data_loader import AbstractDataLoader
from pyodm.core.support.abstract_data_reader import AbstractDataReader
from pyodm.core.xml.reader.configuration.cdisc_configuration_xsd_reader import CdiscConfigurationXsdReader
from pyodm.factory.abstract_hierarchy_factory import AbstractHierarchyFactory
from pyodm.core.json.reader.json_data_reader import JsonDataReader


class CdiscJSONFactory(AbstractHierarchyFactory):
    def __init__(self, data_loader: AbstractDataLoader, configuration_files):
        super().__init__(configuration_files=configuration_files)
        self.data_loader = data_loader

    def clazz_reader(self):
        CdiscConfigurationXsdReader().load_cdisc_definition(self, self._configuration_files)

    def data_reader(self) -> AbstractDataReader:
        return JsonDataReader(self)
