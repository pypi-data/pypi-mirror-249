import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Standard(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Standard
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Type = Model.Attribute()
    
    PublishingSet = Model.Attribute()
    
    Version = Model.Attribute()
    
    Status = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
