import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Location(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Location+Element
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Role = Model.Attribute()
    
    OrganizationOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    MetaDataVersionRef = Model.ManyElements()
    
    Address = Model.ManyElements()
    
    Telecom = Model.ManyElements()
    
    Query = Model.ManyElements()
    
