import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Study(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Study
    """
    
    OID = Model.Attribute()
    
    StudyName = Model.Attribute()
    
    ProtocolName = Model.Attribute()
    
    VersionID = Model.Attribute()
    
    VersionName = Model.Attribute()
    
    Status = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    MetaDataVersion = Model.ManyElements()
    
