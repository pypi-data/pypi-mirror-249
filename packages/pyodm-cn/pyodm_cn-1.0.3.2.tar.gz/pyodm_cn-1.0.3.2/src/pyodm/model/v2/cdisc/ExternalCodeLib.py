import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ExternalCodeLib(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ExternalCodeLib
    """
    
    Library = Model.Attribute()
    
    Method = Model.Attribute()
    
    Version = Model.Attribute()
    
    ref = Model.Attribute()
    
    href = Model.Attribute()
    
    
