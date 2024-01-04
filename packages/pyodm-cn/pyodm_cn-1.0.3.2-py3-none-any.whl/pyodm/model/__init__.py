from pyodm.utils.path_utils import PathUtils


def odm_xsd_description():
    base = PathUtils.folder("pyodm", __file__).joinpath("model", "v2", "resources", "schema")
    xsd_files = ["ODM-admindata.xsd", "ODM-clinicaldata.xsd", "ODM-foundation.xsd",
                 "ODM-protocol.xsd", "ODM-referencedata.xsd", "ODM-study.xsd"]
    return [base.joinpath(xsd) for xsd in xsd_files]


def odm_specification_description():
    base = PathUtils.folder("pyodm", __file__).joinpath("resources")
    files = ["SpecificationV2.xml"]
    return [base.joinpath(file) for file in files]
