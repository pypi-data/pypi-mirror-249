import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyObjective(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyObjective
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Level = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    StudyEndPointRef = Model.ManyElements()
    
