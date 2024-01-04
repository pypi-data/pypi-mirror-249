import abc
from abc import ABC


class AbstractDataSource(ABC):

    def __init__(self):
        self._registry = None

    @abc.abstractmethod
    def read(self): ...
