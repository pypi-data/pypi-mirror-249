import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class TranslatedText(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/TranslatedText
    """
    
    xml_lang = Model.Attribute()
    
    Type = Model.Attribute()
    
    
    xhtml_div = Model.ManyElements()
    
