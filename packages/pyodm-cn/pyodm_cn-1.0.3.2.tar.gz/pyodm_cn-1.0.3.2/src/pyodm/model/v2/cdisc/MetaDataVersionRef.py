import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class MetaDataVersionRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MetaDataVersionRef+Element
    """
    
    StudyOID = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()
    
    EffectiveDate = Model.Attribute()
    
    
