import pytest

from pyodm.core.xml.reader.configuration.cdisc_configuration_specification_reader import \
    CdiscConfigurationSpecificationReader
from pyodm.core.xml.reader.configuration.cdisc_configuration_xsd_reader import CdiscConfigurationXsdReader
from pyodm.factory.cdisc_registry import CdiscRegistry

from pyodm.utils.path_utils import PathUtils


@pytest.fixture
def xsd_files():
    base = PathUtils.folder("pyodm", __file__).joinpath("model", "v2", "resources", "schema")
    xsds = ["ODM-admindata.xsd", "ODM-clinicaldata.xsd", "ODM-foundation.xsd",
            "ODM-protocol.xsd", "ODM-referencedata.xsd", "ODM-study.xsd"]
    return [base.joinpath(xsd) for xsd in xsds]


@pytest.fixture
def specification_file():
    return PathUtils.folder("pyodm", __file__).joinpath("resources", "SpecificationV2.xml")


def test_with_xsd(xsd_files):
    """
    对应 https://wiki.cdisc.org/display/ODM2 检查 Element XPath(s)
    :param xsd_files:
    :type xsd_files:
    :return:
    :rtype:
    """
    registry = CdiscRegistry()
    CdiscConfigurationXsdReader().load_cdisc_definition(registry, xsd_files=xsd_files)
    # for e in registry.definition_tree.xpath("Signature", Direction.TO):
    #     print(e)

    for e in registry.definition_tree.xpath_range("ReferenceData", "Signature"):
        print(e)


def test_with_spec(specification_file):
    registry = CdiscRegistry()
    CdiscConfigurationSpecificationReader().load_cdisc_definition(registry, [specification_file])
    for e in registry.definition_tree.xpath("ODM"):
        print(e)
    registry.definition_tree.children_by_name("SubjectData")