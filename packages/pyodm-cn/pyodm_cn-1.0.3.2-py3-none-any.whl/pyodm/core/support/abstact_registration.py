import abc

from pyodm.factory.cdisc_registry import CdiscRegistry


class AbstractRegistration(abc.ABC):
    def __init__(self):
        self._registry: CdiscRegistry = None

    @property
    def registry(self):
        if self._registry is None: raise Exception("registry is None in Registration")
        return self._registry

    @registry.setter
    def registry(self, value: CdiscRegistry): self._registry = value
