import abc

from pyodm.factory.abstract_cdisc_factory import AbstractCdiscFactory


class AbstractHierarchyFactory(AbstractCdiscFactory, abc.ABC):
    """
    针对 数据源类似 XML 读出数据，
    因为这类型的数据之间包含了层级关系
    """
    def __init__(self, configuration_files: list = None):
        """
        :param configuration_files: 默认是使用 XSD配置文件
        :type configuration_files:
        """
        super().__init__()
        self._configuration_files = configuration_files if configuration_files else self.default_description_files()
