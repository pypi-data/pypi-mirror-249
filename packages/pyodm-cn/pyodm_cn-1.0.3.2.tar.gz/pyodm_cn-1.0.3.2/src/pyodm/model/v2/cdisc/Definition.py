import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Definition(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Definition
    """
    
    
    TranslatedText = Model.ManyElements()
    
