import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Coding(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Coding
    """
    
    Code = Model.Attribute()
    
    System = Model.Attribute()
    
    SystemName = Model.Attribute()
    
    SystemVersion = Model.Attribute()
    
    Label = Model.Attribute()
    
    href = Model.Attribute()
    
    ref = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
