import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Comment(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Comment
    """
    
    SponsorOrSite = Model.Attribute()
    
    
    TranslatedText = Model.ManyElements()
    
