import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Flag(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Flag
    """
    
    
    FlagValue = Model.OneElement()
    
    FlagType = Model.OneElement()
    
