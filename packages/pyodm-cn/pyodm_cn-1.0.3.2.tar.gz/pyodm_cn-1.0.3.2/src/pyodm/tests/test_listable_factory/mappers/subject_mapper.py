from cjen import MetaMysql

from pyodm.model.definition.mapper.assemble import CdiscSQL
from pyodm.utils.path_utils import PathUtils

path = PathUtils.folder("pyodm", __file__)


@CdiscSQL(
    sql_path=path.joinpath("tests", "test_listable_factory", "sqls", "subjects.sql"),
    mapper_path=path.joinpath("tests", "test_listable_factory", "mappers", "mapper.xml"))
class SubjectMapper(MetaMysql): ...
