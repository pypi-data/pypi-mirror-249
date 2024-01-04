import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Query(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Query
    """
    
    OID = Model.Attribute()
    
    Source = Model.Attribute()
    
    Target = Model.Attribute()
    
    Type = Model.Attribute()
    
    State = Model.Attribute()
    
    LastUpdateDatetime = Model.Attribute()
    
    Name = Model.Attribute()
    
    
    Value = Model.OneElement()
    
    AuditRecord = Model.ManyElements()
    
