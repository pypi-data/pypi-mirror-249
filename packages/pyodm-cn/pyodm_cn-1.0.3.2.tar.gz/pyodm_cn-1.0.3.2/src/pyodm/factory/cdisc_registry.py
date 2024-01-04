from pyodm.exceptions import CdiscFactoryException
from pyodm.factory.xpath.xpath_tree import XpathTree


class CdiscRegistry:
    """
    注册 ODM 元素的 Class 类型
    """
    def __init__(self):
        self._registry_classes = dict()
        self.definition_tree = XpathTree()

    def get(self, name: str):
        """
        根据 ODM 的元素名, 获取 ODM Class
        :param name: ODM 元素名
        :type name:
        :return:
        :rtype:
        """
        if self._registry_classes.get(name) is None:
            raise CdiscFactoryException(f"{name} No Registry Class")
        return self._registry_classes.get(name)

    def registry_cdisc(self, name, cdisc_class):
        """
        根据 ODM 元素名, 注册 ODM Class
        :param name:
        :type name:
        :param cdisc_class:
        :type cdisc_class:
        :return:
        :rtype:
        """
        self._registry_classes[name] = cdisc_class
