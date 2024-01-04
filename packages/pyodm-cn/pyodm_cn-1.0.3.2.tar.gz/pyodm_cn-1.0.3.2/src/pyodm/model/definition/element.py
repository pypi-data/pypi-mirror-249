from pyodm.exceptions import ParserException
from pyodm.model.definition.cdisc_model import CdiscModel


class ManyElements(CdiscModel):
    """
    * (meaning optional, with zero or more occurrences)
    + (meaning required, with one or more occurrences)
    对应标识为*或+的子元素
    """

    def __init__(self):
        super().__init__()
        self._array = []

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    @property
    def array(self) -> list:
        return self._array

    def __lshift__(self, other):
        self._array.append(other)

    def index(self, i):
        if i >= self.count: raise ParserException(
            f"{self.get_name} count = {self.count}, i({i}) should less than < {self.count}")
        return self._array[i]

    def first(self):
        """
        :return: 返回第一个节点
        :rtype: CdiscODMEntity
        """
        return self._array[0]

    def find(self, **attributes):
        """
        根据节点属性查找节点
        :param attributes: key 属性名， value 节点值
        :type attributes: **kwargs
        :return: 符合要求的节点 如果没有查询到则返回None
        :rtype: CdiscODMEntity 或 None
        """
        for entity in self.array:
            bingo = True
            for key, value in attributes.items():
                finder = getattr(entity, key, None)

                if finder is None or finder.no_use() or finder.get_value() != value:
                    bingo = False
                    break
            if bingo: return entity
        return None

    @property
    def count(self):
        """
        返回节点数量
        :return:
        :rtype:
        """
        return len(self._array)


class OneElement(CdiscModel):
    """
    ? (meaning optional, with zero or one occurrence)
    """

    def __init__(self):
        super().__init__()
        self._name = "NoUse!"
        self._value = None


    def get_name(self): return self._name

    def set_name(self, value): self._name = value

    def get_value(self): return self._value

    def set_value(self, value): self._value = value

    def is_blank(self) -> bool: return self._value is None
