import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Organization(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Organization+Element
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Role = Model.Attribute()
    
    Type = Model.Attribute()
    
    LocationOID = Model.Attribute()
    
    PartOfOrganizationOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Address = Model.ManyElements()
    
    Telecom = Model.ManyElements()
    
