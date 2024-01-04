import pathlib

from pyodm.core.xml.writer.cdisc_xml_writer import CdiscXmlWriter


def assert_case1(cdisc):
    cw = CdiscXmlWriter(cdisc.odm(), out_put=pathlib.Path("test.xml"))
    cw.write()


def assert_case2(cdisc):
    x = cdisc.odm().ClinicalData.first().SubjectData.first().StudyEventData.first().ItemGroupData.first().ItemData.first().Value
    assert x.first().get_value() == '2200-10-01'
    query = cdisc.odm().ClinicalData.first().SubjectData.first().StudyEventData.first().ItemGroupData.first().ItemData.find().Query.find()
    assert query.Value.get_value() == 'Value 2200-10-01 is in the future, please correct'
    assert query.AuditRecord.first().DateTimeStamp.get_value() == '2021-03-10T13:36:51.668-00:00'
    cw = CdiscXmlWriter(cdisc.odm(), out_put=pathlib.Path("test.xml"))
    cw.write()


def assert_case3(cdisc):
    x = cdisc.odm().ClinicalData
    assert x.first().StudyOID.get_value() == '11'
    assert x.index(1).StudyOID.get_value() == "EX001"
    cw = CdiscXmlWriter(cdisc.odm(), out_put=pathlib.Path("test.xml"))
    cw.write()


def assert_case4(cdisc):
    subject = cdisc.odm().ClinicalData.first().SubjectData.first()
    assert subject.SubjectKey.get_value() == '1001'
    query = subject.StudyEventData.find().ItemGroupData.first().ItemData.first().Query._array
    assert query[0].Value.get_value() == "Value is in the future, please correct"
    for i in query[0].AuditRecord._array:
        print(i.ReasonForChange.get_value())
    cw = CdiscXmlWriter(cdisc.odm(), out_put=pathlib.Path("test.xml"))
    cw.write()


def assert_case5(cdisc):
    cdisc.odm().ClinicalData.usage(lambda x: print(x.first().StudyOID.get_value()))


def assert_case6(cdisc):
    subject = cdisc.odm().ClinicalData.first().SubjectData.first()
    item_group_data = subject.StudyEventData.first().ItemGroupData.find()
    item_group_data1 = item_group_data.ItemGroupData.index(0)
    assert item_group_data1.ItemGroupOID.get_value() == "IG.WBC"
    item_data = item_group_data1.ItemData.find()
    assert item_data.Value.first().get_value() == '5.2'
    item_data = item_group_data1.ItemData.index(1)
    assert item_data.Value.first().get_value() == '10*3/uL'
    item_group_data2 = item_group_data.ItemGroupData.find()
    assert item_group_data2.ItemGroupOID.get_value() == "IT.RBC"
    item_data = item_group_data2.ItemData.first()
    assert item_data.IsNull.get_value() == "Yes"
    cw = CdiscXmlWriter(cdisc.odm(), out_put=pathlib.Path("test.xml"))
    cw.write()
