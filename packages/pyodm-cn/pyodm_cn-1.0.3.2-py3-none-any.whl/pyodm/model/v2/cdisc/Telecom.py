import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Telecom(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Telecom+Element
    """
    
    TelecomType = Model.Attribute()
    
    Value = Model.Attribute()
    
    
