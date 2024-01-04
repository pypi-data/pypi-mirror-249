from pyodm.core.support.abstract_data_source import AbstractDataSource
from pyodm.core.support.abstract_data_loader import AbstractDataLoader
from pyodm.utils.forest import Forest


class ForestDataLoader(AbstractDataLoader):

    def __init__(self, data_source: AbstractDataSource):
        self._data_source = data_source

    def load(self):
        return Forest.transform(self._data_source.read())
