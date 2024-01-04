import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEndPoint(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPoint
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Type = Model.Attribute()
    
    Level = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    FormalExpression = Model.ManyElements()
    
