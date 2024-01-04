import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class AuditRecord(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/AuditRecord+Element
    """
    
    EditPoint = Model.Attribute()
    
    UsedMethod = Model.Attribute()
    
    
    UserRef = Model.OneElement()
    
    LocationRef = Model.OneElement()
    
    DateTimeStamp = Model.OneElement()
    
    ReasonForChange = Model.OneElement()
    
    SourceID = Model.OneElement()
    
