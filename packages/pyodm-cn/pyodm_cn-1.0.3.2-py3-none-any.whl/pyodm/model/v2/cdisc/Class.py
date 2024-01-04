import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Class(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Class
    """
    
    Name = Model.Attribute()
    
    
    SubClass = Model.ManyElements()
    
