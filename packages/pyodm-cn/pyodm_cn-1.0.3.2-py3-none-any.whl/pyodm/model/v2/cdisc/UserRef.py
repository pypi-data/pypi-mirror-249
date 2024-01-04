import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class UserRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/UserRef+Element
    """
    
    UserOID = Model.Attribute()
    
    
