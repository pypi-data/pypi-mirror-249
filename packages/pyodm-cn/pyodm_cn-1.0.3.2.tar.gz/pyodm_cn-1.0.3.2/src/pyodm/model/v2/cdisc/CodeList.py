import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class CodeList(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CodeList
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    DataType = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    StandardOID = Model.Attribute()
    
    IsNonStandard = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    CodeListItem = Model.ManyElements()
    
    Coding = Model.ManyElements()
    
    Alias = Model.ManyElements()
    
