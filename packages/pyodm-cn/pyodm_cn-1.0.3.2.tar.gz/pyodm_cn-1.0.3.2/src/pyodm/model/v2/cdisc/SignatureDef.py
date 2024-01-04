import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class SignatureDef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SignatureDef+Element
    """
    
    OID = Model.Attribute()
    
    Methodology = Model.Attribute()
    
    
    Meaning = Model.OneElement()
    
    LegalReason = Model.OneElement()
    
