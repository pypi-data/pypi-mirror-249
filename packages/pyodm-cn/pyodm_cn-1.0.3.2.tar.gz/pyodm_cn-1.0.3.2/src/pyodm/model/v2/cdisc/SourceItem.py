import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class SourceItem(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SourceItem
    """
    
    ItemOID = Model.Attribute()
    
    ItemGroupOID = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()
    
    StudyOID = Model.Attribute()
    
    leafID = Model.Attribute()
    
    Name = Model.Attribute()
    
    
    Resource = Model.ManyElements()
    
    Coding = Model.ManyElements()
    
