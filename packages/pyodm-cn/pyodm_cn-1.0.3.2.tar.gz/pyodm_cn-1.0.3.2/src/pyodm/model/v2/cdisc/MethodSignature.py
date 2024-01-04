import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class MethodSignature(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MethodSignature
    """
    
    
    Parameter = Model.ManyElements()
    
    ReturnValue = Model.ManyElements()
    
