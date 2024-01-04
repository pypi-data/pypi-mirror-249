import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Arm(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Arm
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    WorkflowRef = Model.OneElement()
    
