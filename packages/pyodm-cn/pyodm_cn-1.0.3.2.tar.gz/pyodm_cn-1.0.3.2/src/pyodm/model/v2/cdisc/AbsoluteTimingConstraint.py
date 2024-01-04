import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class AbsoluteTimingConstraint(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/AbsoluteTimingConstraint
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    StudyEventGroupOID = Model.Attribute()
    
    StudyEventOID = Model.Attribute()
    
    TimepointTarget = Model.Attribute()
    
    TimepointPreWindow = Model.Attribute()
    
    TimepointPostWindow = Model.Attribute()
    
    
    Description = Model.OneElement()
    
