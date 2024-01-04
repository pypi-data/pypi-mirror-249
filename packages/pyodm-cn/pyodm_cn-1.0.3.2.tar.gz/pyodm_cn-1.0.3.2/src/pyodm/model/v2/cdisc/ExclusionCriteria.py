import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ExclusionCriteria(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ExclusionCriteria
    """
    
    
    Criterion = Model.ManyElements()
    
