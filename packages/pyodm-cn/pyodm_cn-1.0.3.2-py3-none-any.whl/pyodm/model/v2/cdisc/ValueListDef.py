import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ValueListDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ValueListDef
    """
    
    OID = Model.Attribute()
    
    
    Description = Model.ManyElements()
    
    ItemRef = Model.ManyElements()
    
