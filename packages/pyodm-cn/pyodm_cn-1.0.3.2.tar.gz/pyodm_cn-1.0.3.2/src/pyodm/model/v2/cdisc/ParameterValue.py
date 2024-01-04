import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ParameterValue(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ParameterValue
    """
    
    Value = Model.Attribute()
    
    
    Coding = Model.ManyElements()
    
