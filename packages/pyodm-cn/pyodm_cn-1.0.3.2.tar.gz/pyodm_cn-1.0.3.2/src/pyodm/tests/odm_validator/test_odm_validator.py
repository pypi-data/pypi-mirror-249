import pytest
import lxml.etree as Etree

from pyodm.utils.validator import Validator

def test_xml_xsd_valid():
    assert Validator.odm("resources/odm_template.xml") == True


def test_xml_xsd_unvalid():
    with pytest.raises(Etree.DocumentInvalid):
        Validator.odm("resources/un_odm_xml.xml")
