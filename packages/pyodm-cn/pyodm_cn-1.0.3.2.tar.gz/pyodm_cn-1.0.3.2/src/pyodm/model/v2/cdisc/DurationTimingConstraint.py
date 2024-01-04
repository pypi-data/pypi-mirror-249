import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class DurationTimingConstraint(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/DurationTimingConstraint
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    StructuralElementOID = Model.Attribute()
    
    DurationTarget = Model.Attribute()
    
    DurationPreWindow = Model.Attribute()
    
    DurationPostWindow = Model.Attribute()
    
    
    Description = Model.OneElement()
    
