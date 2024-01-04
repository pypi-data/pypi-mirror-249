import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyStructure(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyStructure
    """
    
    
    Description = Model.OneElement()
    
    Arm = Model.ManyElements()
    
    Epoch = Model.ManyElements()
    
    WorkflowRef = Model.OneElement()
    
