import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Selection(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Selection
    """
    
    Path = Model.Attribute()
    
    
