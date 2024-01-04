import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyTargetPopulation(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyTargetPopulation
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Coding = Model.ManyElements()
    
    FormalExpression = Model.ManyElements()
    
