import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ReferenceData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ReferenceData
    """
    
    StudyOID = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()
    
    
    ItemGroupData = Model.ManyElements()
    
    AuditRecord = Model.OneElement()
    
    Signature = Model.OneElement()
    
    Annotation = Model.ManyElements()
    
