import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Image(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Image+Element
    """
    
    ImageFileName = Model.Attribute()
    
    href = Model.Attribute()
    
    MimeType = Model.Attribute()
    
    
