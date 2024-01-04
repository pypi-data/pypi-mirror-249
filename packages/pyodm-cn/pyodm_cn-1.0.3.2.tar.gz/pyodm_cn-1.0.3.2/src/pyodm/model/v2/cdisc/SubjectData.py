import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class SubjectData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SubjectData+Element
    """
    
    SubjectKey = Model.Attribute()
    
    TransactionType = Model.Attribute()
    
    
    InvestigatorRef = Model.OneElement()
    
    SiteRef = Model.OneElement()
    
    StudyEventData = Model.ManyElements()
    
    Query = Model.ManyElements()
    
    AuditRecord = Model.OneElement()
    
    Signature = Model.OneElement()
    
    Annotation = Model.ManyElements()
    
