import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class KeySet(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/KeySet
    """
    
    StudyOID = Model.Attribute()
    
    SubjectKey = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()
    
    StudyEventOID = Model.Attribute()
    
    StudyEventRepeatKey = Model.Attribute()
    
    ItemGroupOID = Model.Attribute()
    
    ItemGroupRepeatKey = Model.Attribute()
    
    ItemOID = Model.Attribute()
    
    
