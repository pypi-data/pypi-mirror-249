import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class MethodDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MethodDef
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Type = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    MethodSignature = Model.ManyElements()
    
    FormalExpression = Model.ManyElements()
    
    Alias = Model.ManyElements()
    
    DocumentRef = Model.ManyElements()
    
