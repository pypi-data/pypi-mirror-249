import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class CodeListItem(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CodeListItem
    """
    
    CodedValue = Model.Attribute()
    
    Rank = Model.Attribute()
    
    Other = Model.Attribute()
    
    OrderNumber = Model.Attribute()
    
    ExtendedValue = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Decode = Model.OneElement()
    
    Coding = Model.ManyElements()
    
    Alias = Model.ManyElements()
    
