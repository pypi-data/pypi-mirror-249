import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEventRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventRef
    """
    
    StudyEventOID = Model.Attribute()
    
    OrderNumber = Model.Attribute()
    
    Mandatory = Model.Attribute()
    
    CollectionExceptionConditionOID = Model.Attribute()
    
    
