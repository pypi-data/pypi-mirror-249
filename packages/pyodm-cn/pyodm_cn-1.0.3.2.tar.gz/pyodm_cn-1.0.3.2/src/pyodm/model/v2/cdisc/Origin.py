import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Origin(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Origin
    """
    
    Type = Model.Attribute()
    
    Source = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    SourceItems = Model.OneElement()
    
    Coding = Model.ManyElements()
    
    DocumentRef = Model.ManyElements()
    
