import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Include(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Include
    """
    
    StudyOID = Model.Attribute()
    
    MetaDataVersionOID = Model.Attribute()
    
    href = Model.Attribute()
    
    
