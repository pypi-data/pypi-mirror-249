import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyTiming(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTiming
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    
    AbsoluteTimingConstraint = Model.ManyElements()
    
    RelativeTimingConstraint = Model.ManyElements()
    
    TransitionTimingConstraint = Model.ManyElements()
    
    DurationTimingConstraint = Model.ManyElements()
    
