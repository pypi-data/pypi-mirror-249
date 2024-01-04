
from pyodm.utils.search.odm_dfs import ODMDfs
from pyodm.utils.odm_utils import OdmUtils


class Stream:
    def __init__(self, data):
        self.dfs = self.dfs_clazz()(data)

    def find(self, _lambda):
        return Optional(self.dfs.find(_lambda=_lambda))

    def dfs_clazz(self): return ODMDfs


class Optional:
    def __init__(self, data):
        self._data = data

    def get(self):
        return self._data

    def find(self, _lambda):
        return self.as_stream().find(_lambda=_lambda)

    def update(self, **attributes):
        """
        更新 ODM 的属性
        :param attributes:
        :type attributes:
        :return:
        :rtype:
        """
        for name, value in attributes.items():
            self._data.__dict__.get(name).set_value(value)
        return self

    def update_text(self, value):
        """
        更新 ODM 的文本值
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self._data.set_value(value)
        return self

    def merge(self, odm_element):
        """
        合并 两个 ODM ELEMENT
        前提是 被合并对象 odm_element 与 合并对象的 根节点一致
        OneElement ,以当前元素为基准，合并属性，并且 合并子元素
        ManyElement , 在原有的元素上，添加新的元素
        :param odm_element:
        :type odm_element:
        :return:
        :rtype:
        """
        if self._data.get_name() != odm_element.get_name():
            raise Exception(f'{self._data.get_name()} is different {odm_element.get_name()}')
        OdmUtils.merge(self._data, odm_element)

    def replace(self, name, odm_element):
        """
        替换指定的子元素
        :param name: element name
        :type name: str
        :param odm_element: 替换的元素
        :type odm_element:
        :return:
        :rtype:
        """
        if self._data.__dict__.get(name) is None: raise Exception(f'{self._data.get_name()} have not element {name}')
        replaced = self._data.__dict__.get(name)
        """处理 OneElement 和 实例 直接替换"""
        if OdmUtils.is_entity(replaced) or OdmUtils.is_one_element(replaced):
            setattr(self._data, name, odm_element)
        """处理ManyElements"""
        if OdmUtils.is_many_elements(replaced):
            """如果 为空，则直接增加一个项 """
            if OdmUtils.useless(self._data, name):
                self.append(name, odm_element)
            else:
                """如果 不为空，则查找相似的替换 """
                for i in range(len(replaced.array)):
                    if OdmUtils.like(replaced.index(i), odm_element):
                        replaced.array[i] = odm_element
                        break

    def append(self, name, odm_element):
        """
        ManyElements 添加一个元素
        :return:
        :rtype:
        """
        if OdmUtils.is_many_elements(self._data.__dict__.get(name)):
            if OdmUtils.useless(self._data, name):  self._data.__dict__.get(name).set_name(name)
            OdmUtils.append(self._data.__dict__.get(name), odm_element)
        else:
            raise Exception(f"{name} is not ManyElements")

    def add(self, element_entity):
        """
        增加一个 OneElement 实例
        前提是：
        1. 新增的 OneElement 存在
        2. OneElement 还没有被实例化
        :param element_entity:  Element 的实例
        :type element_entity:
        :return:
        :rtype:
        """
        if not OdmUtils.is_one_element(self._data.__dict__.get(element_entity.get_name())):
            raise Exception(f'{element_entity.get_name()} is not OneElement')
        OdmUtils.add(self._data, element_entity)


    def as_stream(self):
        return Stream(self._data)
