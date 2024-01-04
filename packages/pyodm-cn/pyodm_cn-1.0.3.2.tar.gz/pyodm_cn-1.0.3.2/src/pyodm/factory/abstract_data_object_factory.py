import abc

from pyodm.core.support.abstract_data_loader import AbstractDataLoader
from pyodm.core.support.abstract_data_reader import AbstractDataReader

from pyodm.factory.cdisc_registry import CdiscRegistry


class AbstractDataObjectFactory(abc.ABC, CdiscRegistry):

    def __init__(self):
        super().__init__()
        self._data_object = None
        self._data_loader = None

    @abc.abstractmethod
    def clazz_reader(self):
        """
        指定 生成 ODM Class 的方式
        :return:
        :rtype:
        """
        ...

    @abc.abstractmethod
    def data_reader(self) -> AbstractDataReader:
        """
        指定 解析 ODM Data 的方式
        :return:
        :rtype:
        """
        ...

    @property
    def data_loader(self):
        """
        读取 ODM 数据
        :return:
        :rtype:
        """
        return self._data_loader

    @data_loader.setter
    def data_loader(self, data_loader: AbstractDataLoader):
        self._data_loader = data_loader

    def _data_process(self, specified: str = None, refresh: bool = False):
        """
        解析 ODM Data 模板方法
        :param specified: 指定 要读取的 ODM 对象
        :type: str
        :param refresh: 是否重新读取 True Y, False N
        :type refresh: bool
        :return:
        :rtype:
        """
        __new = True if self._data_object is None else refresh
        if __new:
            self.clazz_reader()
            if specified is None:
                self._data_object = self.data_reader().read(self.data_loader)
            else:
                self._data_object = self.data_reader().read_specified(specified, self.data_loader)
        return self._data_object

    def factory(self, specified: str = None, refresh: bool = False):
        return self._data_process(specified, refresh)
