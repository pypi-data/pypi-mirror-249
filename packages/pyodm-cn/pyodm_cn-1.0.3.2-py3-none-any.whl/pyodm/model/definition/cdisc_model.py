from pyodm.model.definition.usage import Usage


class CdiscModel:
    def __init__(self):
        self._preset_usage: Usage = None
        self._name = "NoUse!"
        self._parent = None

    def find(self, **attributes):
        raise Exception(f"{self.get_name} is not ManyElements, Only ManyElements have")

    @property
    def preset_usage(self):
        """
        获取预置的 业务处理
        :return:
        :rtype:
        """
        return self._preset_usage

    @preset_usage.setter
    def preset_usage(self, value):
        """
        设置预置的 业务处理
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self._preset_usage = value

    def first(self):
        raise Exception(f"{self.get_name} is not ManyElements, Only ManyElements have")

    def index(self, i):
        raise Exception(f"{self.get_name} is not ManyElements, Only ManyElements have")


    def get_name(self):
        raise Exception("CdiscModel must defined name")


    def set_name(self, value): self._name = value

    def get_value(self):
        raise Exception(f"{self.get_name()} is not ManyElements, ManyElements is not have this method")


    # TODO
    def each(self, usage, **attributes):
        raise Exception(f"{self.get_name()} is not ManyElements, Only ManyElements have")

    # TODO
    def select(self, **attributes):
        raise Exception(f"{self.get_name()} is not ManyElements, Only ManyElements have")

    def business(self):
        """
        执行预置的 业务处理
        :return:
        :rtype:
        """
        if self.preset_usage is not None:
            self.preset_usage.business(self)

    def usage(self, usage):
        """
        执行针对该节点的业务逻辑
        usage 为传入
        :param usage: 需要处理的业务逻辑
        :type usage: lambda, 函数，或 Usage 类型的实例
        :return:
        :rtype:
        """
        if callable(usage):  # lambda, 函数判断
            usage(self)
        elif isinstance(usage, Usage):  # 实例判断
            usage.business(self)

    def no_use(self):
        return self.get_name() == "NoUse!"

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
