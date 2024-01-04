import abc


class AbstractDataLoader(abc.ABC):
    @abc.abstractmethod
    def load(self):
        """
        读取数据源，转化为期望的数据结构
        :return:
        :rtype:
        """
        ...
