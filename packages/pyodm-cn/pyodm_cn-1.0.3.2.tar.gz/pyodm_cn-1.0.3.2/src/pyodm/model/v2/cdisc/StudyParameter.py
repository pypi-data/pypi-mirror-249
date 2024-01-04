import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyParameter(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyParameter
    """
    
    OID = Model.Attribute()
    
    Term = Model.Attribute()
    
    ShortName = Model.Attribute()
    
    
    ParameterValue = Model.ManyElements()
    
    Coding = Model.ManyElements()
    
