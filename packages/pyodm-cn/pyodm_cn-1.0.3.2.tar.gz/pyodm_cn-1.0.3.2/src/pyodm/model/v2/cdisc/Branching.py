import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Branching(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Branching
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Type = Model.Attribute()
    
    
    TargetTransition = Model.ManyElements()
    
    DefaultTransition = Model.ManyElements()
    
