import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class SourceItems(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/SourceItems
    """
    
    
    SourceItem = Model.ManyElements()
    
    Coding = Model.ManyElements()
    
