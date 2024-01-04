import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class AdminData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/AdminData+Element
    """
    
    StudyOID = Model.Attribute()
    
    
    User = Model.ManyElements()
    
    Organization = Model.ManyElements()
    
    Location = Model.ManyElements()
    
    SignatureDef = Model.ManyElements()
    
