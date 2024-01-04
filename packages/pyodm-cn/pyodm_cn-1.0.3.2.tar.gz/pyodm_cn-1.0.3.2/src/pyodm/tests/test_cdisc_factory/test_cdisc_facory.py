
import pytest

from pyodm.core.source.path_source import PathSource
from pyodm.factory.cdsic_xml_xsd_factory import CdiscXMLXsdFactory
from pyodm.tests.test_cdisc_factory.common_assert import assert_case1, assert_case2, \
    assert_case3, assert_case4, assert_case5, assert_case6
from pyodm.utils.path_utils import PathUtils


@pytest.fixture
def xsd_files():
    base = PathUtils.folder("pyodm", __file__).joinpath("model", "v2", "resources", "schema")
    xsds = ["ODM-admindata.xsd", "ODM-clinicaldata.xsd", "ODM-foundation.xsd",
            "ODM-protocol.xsd", "ODM-referencedata.xsd", "ODM-study.xsd"]
    return [base.joinpath(xsd) for xsd in xsds]


def test_case1(xsd_files):
    xsd_file = [xsd_files[0]]
    data_file = PathSource("resources", "data", "user.xml")
    cdisc = CdiscXMLXsdFactory(data_file=data_file, xsd_files=xsd_file)
    assert_case1(cdisc)


def test_case2(xsd_files):
    data_file = PathSource("resources", "data", "odm_template.xml")
    cdisc = CdiscXMLXsdFactory(data_file=data_file, xsd_files=xsd_files)
    assert_case2(cdisc)


def test_case3(xsd_files):
    data_file = PathSource("resources", "data", "test_case2.xml")
    cdisc = CdiscXMLXsdFactory(data_file=data_file, xsd_files=xsd_files)
    assert_case3(cdisc)


def test_case4(xsd_files):
    data_file = PathSource("resources", "data", "transaction_history.xml")
    cdisc = CdiscXMLXsdFactory(data_file=data_file, xsd_files=xsd_files)
    assert_case4(cdisc)


def test_case5(xsd_files):
    data_file = PathSource("resources", "data", "transaction_history.xml")
    cdisc = CdiscXMLXsdFactory(data_file=data_file, xsd_files=xsd_files)
    assert_case5(cdisc)


def test_case6(xsd_files):
    data_file = PathSource("resources", "data", "odm_testcase5.xml")
    cdisc = CdiscXMLXsdFactory(data_file=data_file, xsd_files=xsd_files)
    assert_case6(cdisc)
