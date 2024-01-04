import pathlib

from pyodm.core.source.path_source import PathSource
from pyodm.core.xml.reader.configuration.cdisc_configuration_xsd_reader import CdiscConfigurationXsdReader
from pyodm.factory.abstract_cdisc_xml_factory import AbstractCdiscXMLFactory
from pyodm.model import odm_xsd_description


class CdiscXMLXsdFactory(AbstractCdiscXMLFactory):
    """
    Class 类型的定义在XSD文件中
    """

    def default_description_files(self) -> list:
        return odm_xsd_description()

    def __init__(self, data_file: PathSource, xsd_files: list = None):
        """
        :param data_file:  数据文件路径
        :type data_file: pathlib.Path
        :param xsd_files: XSD配置文件路径, 默认使用内置的 ODM 配置
        :type xsd_files: list[pathlib.Path]
        """
        super().__init__(data_file, xsd_files)
        self._xsd_files = xsd_files if xsd_files else self.default_description_files()

    def clazz_reader(self):
        """
        使用 XSD 的方式 解析 ODM Class 信息
        :return:
        :rtype:
        """
        CdiscConfigurationXsdReader().load_cdisc_definition(self, self._xsd_files)
