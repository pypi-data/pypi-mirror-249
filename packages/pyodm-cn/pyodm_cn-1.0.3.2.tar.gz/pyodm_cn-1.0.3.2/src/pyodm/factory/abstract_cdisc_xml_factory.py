import pathlib
from abc import ABC

from pyodm.core.data_loader.xml_path_loader import XmlPathLoader
from pyodm.core.source.path_source import PathSource
from pyodm.core.xml.reader.data.xml_data_reader import XMLDataReader
from pyodm.factory.abstract_cdisc_factory import AbstractCdiscFactory
from pyodm.factory.abstract_hierarchy_factory import AbstractHierarchyFactory


class AbstractCdiscXMLFactory(AbstractHierarchyFactory, ABC):
    """
    通过 XML 生成ODM的工程对象的类型，定义了生成模板
        1. 获取 Class 类型 class_reader
        2. 读取 XML 文件转化为ODM 对象 data_reader
    """

    def __init__(self, data_file_path: PathSource, configuration_files: list = None):
        super().__init__(configuration_files)
        self._data_file = data_file_path.read()
        self.data_loader = XmlPathLoader(self._data_file)

    def data_reader(self) -> XMLDataReader:
        """
        指定了解析 ODM XML Data 的数据方式
        :return:
        :rtype:
        """
        return XMLDataReader(self)


