import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEstimand(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEstimand
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    Level = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    StudyTargetPopulationRef = Model.OneElement()
    
    StudyInterventionRef = Model.OneElement()
    
    StudyEndPointRef = Model.OneElement()
    
    IntercurrentEvent = Model.ManyElements()
    
    SummaryMeasure = Model.OneElement()
    
