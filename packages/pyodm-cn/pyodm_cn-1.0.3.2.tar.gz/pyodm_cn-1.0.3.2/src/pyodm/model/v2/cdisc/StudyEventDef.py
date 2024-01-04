import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEventDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEventDef
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Repeating = Model.Attribute()
    
    Type = Model.Attribute()
    
    Category = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    ItemGroupRef = Model.ManyElements()
    
    WorkflowRef = Model.OneElement()
    
    Coding = Model.ManyElements()
    
    Alias = Model.ManyElements()
    
