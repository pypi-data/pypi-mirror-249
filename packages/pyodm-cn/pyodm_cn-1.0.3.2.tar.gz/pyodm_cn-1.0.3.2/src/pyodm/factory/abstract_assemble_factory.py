import abc

from pyodm.core.xml.reader.configuration.cdisc_configuration_xsd_reader import CdiscConfigurationXsdReader
from pyodm.factory.abstract_cdisc_factory import AbstractCdiscFactory


class AbstractAssembleFactory(AbstractCdiscFactory, abc.ABC):
    """
    设置 解析 ODM Class 的方式
    通过 修改 reader_class, 不同的 reader_class 要对应不同 configuration_files
    CdiscConfigurationXsdReader(默认) - odm_xsd_description
    CdiscConfigurationSpecificationReader - odm_specification_description
    """
    def __init__(self, configuration_files: list = None):
        super().__init__()
        self._configuration_files = configuration_files if configuration_files else self.default_description_files()
        self._reader_class = CdiscConfigurationXsdReader

    @property
    def reader_class(self):
        """
        设置 解析 ODM Class的方式
        CdiscConfigurationXsdReader | CdiscConfigurationSpecificationReader
        :return:
        :rtype:
        """
        return self._reader_class

    @reader_class.setter
    def reader_class(self, clazz): self._reader_class = clazz

    def clazz_reader(self):
        """
        根据 reader_class 生成 解析 ODM Class 类，并注册 ODM Class
        :return:
        :rtype:
        """
        self._reader_class().load_cdisc_definition(self, self._configuration_files)