import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class TargetTransition(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TargetTransition
    """
    
    TargetTransitionOID = Model.Attribute()
    
    ConditionOID = Model.Attribute()
    
    
