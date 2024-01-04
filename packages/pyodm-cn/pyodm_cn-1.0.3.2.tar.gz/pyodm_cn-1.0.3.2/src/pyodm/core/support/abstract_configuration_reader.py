import abc
import pathlib

from pyodm.factory.cdisc_registry import CdiscRegistry


class AbstractConfigurationReader(abc.ABC):
    """
    读取配置文件的抽象方法定义，load_cdisc_definition()
    """
    @abc.abstractmethod
    def load_cdisc_definition(self, registry: CdiscRegistry, files: list[pathlib.Path]):
        """
        读取配置文件, 解析 ODM Class信息，并注册进CdiscRegistry对象
        :param registry: 存储 CdiscRegistry 的对象
        :type registry:
        :param files: 配置文件
        :type files:
        :return:
        :rtype:
        """
        ...
