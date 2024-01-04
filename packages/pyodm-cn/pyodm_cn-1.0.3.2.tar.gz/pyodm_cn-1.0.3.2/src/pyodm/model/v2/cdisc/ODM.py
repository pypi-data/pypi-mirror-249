import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ODM(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ODM
    """
    
    FileType = Model.Attribute()
    
    Granularity = Model.Attribute()
    
    Context = Model.Attribute()
    
    FileOID = Model.Attribute()
    
    CreationDateTime = Model.Attribute()
    
    PriorFileOID = Model.Attribute()
    
    AsOfDateTime = Model.Attribute()
    
    ODMVersion = Model.Attribute()
    
    Originator = Model.Attribute()
    
    SourceSystem = Model.Attribute()
    
    SourceSystemVersion = Model.Attribute()
    
    
    Description = Model.ManyElements()
    
    Study = Model.ManyElements()
    
    AdminData = Model.ManyElements()
    
    ReferenceData = Model.ManyElements()
    
    ClinicalData = Model.ManyElements()
    
    Association = Model.ManyElements()
    
