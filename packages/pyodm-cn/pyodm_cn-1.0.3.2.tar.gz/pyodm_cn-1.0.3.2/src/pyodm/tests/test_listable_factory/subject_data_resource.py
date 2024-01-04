import cjen

from cjen.nene.helper import FileHelper

from pyodm.core.source.abstract_database_source import AbstractDataBaseSource
from pyodm.tests.test_listable_factory.mappers.subject_mapper import SubjectMapper


class SubjectDataResource(AbstractDataBaseSource):

    def read(self) -> list[list[dict]]:
        return self.subjects()

    def __init__(self, database_info):
        super().__init__(database_info)

    @cjen.operate.mysql.factory(
        clazz=SubjectMapper,
        sql=FileHelper.read(SubjectMapper.sql_file),
        size=-1
    )
    def subjects(self, subject_mappers: list[SubjectMapper] = None, **kwargs):
        return [subject_mapper(self.registry) for subject_mapper in subject_mappers]
        # return [subject_mapper.mapper(self.registry) for subject_mapper in subject_mappers]
