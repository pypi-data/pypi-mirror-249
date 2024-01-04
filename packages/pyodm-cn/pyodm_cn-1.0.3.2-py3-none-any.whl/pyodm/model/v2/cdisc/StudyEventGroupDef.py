import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEventGroupDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventGroupDef
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    ArmOID = Model.Attribute()
    
    EpochOID = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    WorkflowRef = Model.OneElement()
    
    Coding = Model.ManyElements()
    
    StudyEventGroupRef = Model.OneElement()
    
    StudyEventRef = Model.OneElement()
    
