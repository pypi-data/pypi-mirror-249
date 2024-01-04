import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ItemGroupDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupDef
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Repeating = Model.Attribute()
    
    RepeatingLimit = Model.Attribute()
    
    IsReferenceData = Model.Attribute()
    
    Structure = Model.Attribute()
    
    ArchiveLocationID = Model.Attribute()
    
    DatasetName = Model.Attribute()
    
    Domain = Model.Attribute()
    
    Type = Model.Attribute()
    
    Purpose = Model.Attribute()
    
    StandardOID = Model.Attribute()
    
    IsNonStandard = Model.Attribute()
    
    HasNoData = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Class = Model.ManyElements()
    
    Coding = Model.ManyElements()
    
    WorkflowRef = Model.ManyElements()
    
    Origin = Model.ManyElements()
    
    Alias = Model.ManyElements()
    
    Leaf = Model.ManyElements()
    
    ItemGroupRef = Model.OneElement()
    
    ItemRef = Model.OneElement()
    
