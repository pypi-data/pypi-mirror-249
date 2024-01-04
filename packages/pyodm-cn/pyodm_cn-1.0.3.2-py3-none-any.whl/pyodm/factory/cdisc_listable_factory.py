from pyodm.core.data_loader.forest_data_loader import ForestDataLoader
from pyodm.core.forest.reader.forest_data_reader import ForestDataReader

from pyodm.core.support.abstract_data_source import AbstractDataSource

from pyodm.factory.abstract_assemble_factory import AbstractAssembleFactory


class CdiscListableFactory(AbstractAssembleFactory):
    """
    针对 数据源类似从数据库读出的数据，
    因为这类型的数据之间并没有层级关系，需要把平行数据转化为树形数据的情况
    """

    def __init__(self, source: AbstractDataSource, configuration_files: list = None):
        """

        :param source:
        :type source:
        :param configuration_files: 默认是使用 XSD配置文件
        :type configuration_files:
        """
        super().__init__()
        self._configuration_files = configuration_files if configuration_files else self.default_description_files()
        source.registry = self
        self.data_loader = ForestDataLoader(source)

    def data_reader(self) -> ForestDataReader:
        return ForestDataReader(self)
