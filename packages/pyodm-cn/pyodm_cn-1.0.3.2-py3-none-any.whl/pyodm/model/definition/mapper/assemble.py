from pathlib import Path

from pyodm.core.data_loader.xml_path_loader import XmlPathLoader
from pyodm.core.xml.reader.mapper.xml_mapper_reader import XMLMapperReader
from pyodm.factory.cdisc_registry import CdiscRegistry


def CdiscSQL(sql_path: Path, mapper_path: Path):
    def __inner__(cls):
        return cdisc_sql_factory(cls, sql_path, mapper_path)

    return __inner__


def cdisc_sql_factory(clazz, sql_path: Path, mapper_path: Path):
    setattr(clazz, "sql_file", sql_path)
    setattr(clazz, "mapper_file", mapper_path)
    setattr(clazz, "isCdiscMapper", True)
    setattr(clazz, "__call__", __mapper)
    return clazz


def __mapper(self, registry: CdiscRegistry):
    if self.isCdiscMapper:
        elements = XMLMapperReader(registry, self).read(XmlPathLoader(self.mapper_file))
        return elements
    return []
