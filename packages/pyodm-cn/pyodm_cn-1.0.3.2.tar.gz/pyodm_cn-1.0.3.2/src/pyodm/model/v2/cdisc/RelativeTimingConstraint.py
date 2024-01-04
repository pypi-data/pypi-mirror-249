import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class RelativeTimingConstraint(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/RelativeTimingConstraint
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    PredecessorOID = Model.Attribute()
    
    SuccessorOID = Model.Attribute()
    
    Type = Model.Attribute()
    
    TimepointRelativeTarget = Model.Attribute()
    
    TimepointPreWindow = Model.Attribute()
    
    TimepointPostWindow = Model.Attribute()
    
    
    Description = Model.OneElement()
    
