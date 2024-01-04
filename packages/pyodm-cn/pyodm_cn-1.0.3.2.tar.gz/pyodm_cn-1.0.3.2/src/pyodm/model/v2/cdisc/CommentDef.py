import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class CommentDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/CommentDef
    """
    
    OID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    DocumentRef = Model.ManyElements()
    
