import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ItemDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemDef
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    DataType = Model.Attribute()
    
    Length = Model.Attribute()
    
    DisplayFormat = Model.Attribute()
    
    VariableSet = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Definition = Model.OneElement()
    
    Question = Model.OneElement()
    
    Prompt = Model.OneElement()
    
    CRFCompletionInstructions = Model.OneElement()
    
    ImplementationNotes = Model.OneElement()
    
    CDISCNotes = Model.OneElement()
    
    RangeCheck = Model.ManyElements()
    
    CodeListRef = Model.ManyElements()
    
    ValueListRef = Model.ManyElements()
    
    Coding = Model.ManyElements()
    
    Alias = Model.ManyElements()
    
