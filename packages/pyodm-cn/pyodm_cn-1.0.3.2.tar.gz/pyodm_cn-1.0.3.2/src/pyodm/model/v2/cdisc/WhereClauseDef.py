import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class WhereClauseDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/WhereClauseDef
    """
    
    OID = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    RangeCheck = Model.ManyElements()
    
