import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Prompt(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Prompt
    """
    
    
    TranslatedText = Model.ManyElements()
    
