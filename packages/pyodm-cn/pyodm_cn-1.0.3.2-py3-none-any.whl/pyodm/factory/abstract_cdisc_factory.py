import abc

from pyodm.factory.abstract_data_object_factory import AbstractDataObjectFactory

from pyodm.model import odm_xsd_description


class AbstractCdiscFactory(AbstractDataObjectFactory, abc.ABC):
    """
    生成 ODM 的抽象工厂,定义类生成ODM实例的模板方法

    """

    def default_description_files(self) -> list:
        """
        默认的 XSD 文件路径 , 如果没有指定
        clazz_reader,默认采取的是XSD 的方式解析 ODM Class
        :return:
        :rtype:
        """
        return odm_xsd_description()

    def odm(self, refresh: bool = False):
        """
        返回 ODM 对象
        :param refresh:
        :type refresh:
        :return:
        :rtype:
        """
        return self.factory(refresh=refresh)
