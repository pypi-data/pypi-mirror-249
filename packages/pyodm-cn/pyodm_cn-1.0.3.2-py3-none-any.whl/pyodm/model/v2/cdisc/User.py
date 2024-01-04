import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class User(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/User+Element
    """
    
    OID = Model.Attribute()
    
    UserType = Model.Attribute()
    
    OrganizationOID = Model.Attribute()
    
    LocationOID = Model.Attribute()
    
    
    UserName = Model.OneElement()
    
    Prefix = Model.OneElement()
    
    Suffix = Model.OneElement()
    
    FullName = Model.OneElement()
    
    GivenName = Model.OneElement()
    
    FamilyName = Model.OneElement()
    
    Image = Model.OneElement()
    
    Address = Model.ManyElements()
    
    Telecom = Model.ManyElements()
    
