import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Leaf(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Leaf
    """
    
    ID = Model.Attribute()
    
    xlink_href = Model.Attribute()
    
    
    Title = Model.ManyElements()
    
