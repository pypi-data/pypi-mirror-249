import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ClinicalData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ClinicalData+Element
    """
    
    StudyOID = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()
    
    
    SubjectData = Model.ManyElements()
    
    ItemGroupData = Model.ManyElements()
    
    Query = Model.ManyElements()
    
    AuditRecord = Model.OneElement()
    
    Signature = Model.OneElement()
    
    Annotation = Model.ManyElements()
    
