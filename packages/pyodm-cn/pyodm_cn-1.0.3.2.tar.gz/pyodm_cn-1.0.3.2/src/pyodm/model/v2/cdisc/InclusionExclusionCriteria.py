import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class InclusionExclusionCriteria(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/InclusionExclusionCriteria
    """
    
    
    InclusionCriteria = Model.OneElement()
    
    ExclusionCriteria = Model.OneElement()
    
