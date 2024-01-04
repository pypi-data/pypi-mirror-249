import pathlib
from abc import ABC

from pyodm.core.support.abstract_data_loader import AbstractDataLoader


class AbstractPathDataLoader(AbstractDataLoader, ABC):
    def __init__(self, file: pathlib.Path):
        self.file = file
