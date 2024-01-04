import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Criterion(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Criterion
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    ConditionOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Coding = Model.ManyElements()
    
