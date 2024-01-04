import pathlib

from pyodm.core.support.abstract_data_source import AbstractDataSource


class PathSource(AbstractDataSource):

    def __init__(self, *paths):
        super().__init__()
        self._paths = paths

    def read(self) -> pathlib.Path:
        path = pathlib.Path()
        for value in self._paths:
            path = path.joinpath(value)
        return path
