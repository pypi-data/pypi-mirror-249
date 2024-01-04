import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class TransitionTimingConstraint(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TransitionTimingConstraint
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    TransitionOID = Model.Attribute()
    
    MethodOID = Model.Attribute()
    
    Type = Model.Attribute()
    
    TimepointTarget = Model.Attribute()
    
    TimepointPreWindow = Model.Attribute()
    
    TimepointPostWindow = Model.Attribute()
    
    
    Description = Model.OneElement()
    
