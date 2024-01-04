import abc
from abc import ABC

from cjen.db_bigtangerine import DBBigTangerine

from pyodm.core.support.abstact_registration import AbstractRegistration
from pyodm.core.support.abstract_data_source import AbstractDataSource


class AbstractDataBaseSource(DBBigTangerine, AbstractDataSource, AbstractRegistration, ABC):

    def __init__(self, database_info):
        super().__init__(database_info)

    @abc.abstractmethod
    def read(self) -> list[list[dict]]: ...
