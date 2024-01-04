import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class RangeCheck(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/RangeCheck
    """
    
    Comparator = Model.Attribute()
    
    SoftHard = Model.Attribute()
    
    ItemOID = Model.Attribute()
    
    
    ErrorMessage = Model.ManyElements()
    
