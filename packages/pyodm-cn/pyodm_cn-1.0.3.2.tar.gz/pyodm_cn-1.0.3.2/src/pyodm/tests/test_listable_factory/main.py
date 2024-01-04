import pathlib

from cjen.nene.database_info import DataBaseInfo

from pyodm.core.xml.writer.cdisc_xml_writer import CdiscXmlWriter
from pyodm.factory.cdisc_listable_factory import CdiscListableFactory

from pyodm.tests.test_listable_factory.subject_data_resource import SubjectDataResource
from pyodm.utils.path_utils import PathUtils


def xsd_files():
    base = PathUtils.folder("pyodm", __file__).joinpath("model", "v2", "resources", "schema")
    xsds = ["ODM-admindata.xsd", "ODM-clinicaldata.xsd", "ODM-foundation.xsd",
            "ODM-protocol.xsd", "ODM-referencedata.xsd", "ODM-study.xsd"]
    return [base.joinpath(xsd) for xsd in xsds]


if __name__ == '__main__':
    database_info = DataBaseInfo.factory(dict(
        host="",  # 数据库主机 dev03
        port=3306,  # 数据库端口号
        user="",  # 数据库用户名
        pwd="",  # 数据库密码
        database=""  # 数据库库名 eclinical_edc_dev_846
    ))
    data_source = SubjectDataResource(database_info)
    factory = CdiscListableFactory(data_source, xsd_files())

    odm_data = factory.odm()
    cw = CdiscXmlWriter(odm_data, pathlib.Path(f"result.xml"))
    cw.write()
