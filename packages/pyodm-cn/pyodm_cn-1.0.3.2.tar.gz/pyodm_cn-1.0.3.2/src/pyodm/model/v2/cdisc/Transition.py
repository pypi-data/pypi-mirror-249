import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Transition(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Transition
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    SourceOID = Model.Attribute()
    
    TargetOID = Model.Attribute()
    
    StartConditionOID = Model.Attribute()
    
    EndConditionOID = Model.Attribute()
    
    
