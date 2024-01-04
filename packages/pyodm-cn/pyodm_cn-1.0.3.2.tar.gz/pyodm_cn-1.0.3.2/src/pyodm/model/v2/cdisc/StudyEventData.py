import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEventData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventData+Element
    """
    
    StudyEventOID = Model.Attribute()
    
    StudyEventRepeatKey = Model.Attribute()
    
    TransactionType = Model.Attribute()
    
    
    ItemGroupData = Model.ManyElements()
    
    Query = Model.ManyElements()
    
    AuditRecord = Model.OneElement()
    
    Signature = Model.OneElement()
    
    Annotation = Model.ManyElements()
    
