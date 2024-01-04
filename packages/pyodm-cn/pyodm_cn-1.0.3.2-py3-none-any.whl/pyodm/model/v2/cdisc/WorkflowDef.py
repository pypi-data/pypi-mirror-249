import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class WorkflowDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WorkflowDef
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    WorkflowStart = Model.OneElement()
    
    WorkflowEnd = Model.ManyElements()
    
    Transition = Model.OneElement()
    
    Branching = Model.OneElement()
    
