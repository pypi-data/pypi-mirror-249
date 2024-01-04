import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Signature(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Signature+Element
    """
    
    ID = Model.Attribute()
    
    
    UserRef = Model.OneElement()
    
    LocationRef = Model.OneElement()
    
    SignatureRef = Model.OneElement()
    
    DateTimeStamp = Model.OneElement()
    
