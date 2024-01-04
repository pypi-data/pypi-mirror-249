import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Alias(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Alias
    """
    
    Context = Model.Attribute()
    
    Name = Model.Attribute()
    
    
