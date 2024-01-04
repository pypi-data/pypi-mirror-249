import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Epoch(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Epoch
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    SequenceNumber = Model.Attribute()
    
    
    Description = Model.OneElement()
    
