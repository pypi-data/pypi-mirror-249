import pathlib

from pyodm.core.source.path_source import PathSource
from pyodm.core.xml.reader.data.xml_data_reader import XMLDataReader
from pyodm.core.xml.reader.configuration.cdisc_configuration_specification_reader import \
    CdiscConfigurationSpecificationReader
from pyodm.factory.abstract_cdisc_xml_factory import AbstractCdiscXMLFactory
from pyodm.model import odm_specification_description


class CdiscXMLSpecificationFactory(AbstractCdiscXMLFactory):
    """
    Class 类型的对象定义在Specification 中
    """

    def default_description_files(self) -> list:
        return odm_specification_description()

    def __init__(self, data_file: PathSource, specification_files: list = None):
        """
        :param data_file: 数据文件路径
        :type data_file: pathlib.Path
        :param specification_files: 定义 Class 的配置, 默认使用内置的 ODM 配置
        :type specification_files: list[pathlib.Path]
        """
        super().__init__(data_file, specification_files)
        self._specification_files = specification_files if specification_files else self.default_description_files()

    def clazz_reader(self):
        """
        使用 Specification 的方式 解析 ODM Class 信息
        :return:
        :rtype:
        """
        CdiscConfigurationSpecificationReader().load_cdisc_definition(self, self._specification_files)


