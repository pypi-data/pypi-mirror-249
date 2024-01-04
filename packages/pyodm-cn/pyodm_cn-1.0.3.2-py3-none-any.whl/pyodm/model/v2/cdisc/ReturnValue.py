import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ReturnValue(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ReturnValue
    """
    
    Name = Model.Attribute()
    
    DataType = Model.Attribute()
    
    Definition = Model.Attribute()
    
    OrderNumber = Model.Attribute()
    
    
