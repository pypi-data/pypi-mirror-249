import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Resource(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Resource
    """
    
    Type = Model.Attribute()
    
    Name = Model.Attribute()
    
    Attribute = Model.Attribute()
    
    Label = Model.Attribute()
    
    
    Selection = Model.ManyElements()
    
