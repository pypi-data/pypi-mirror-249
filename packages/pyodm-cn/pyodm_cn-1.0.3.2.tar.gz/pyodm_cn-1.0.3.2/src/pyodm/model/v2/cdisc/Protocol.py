import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class Protocol(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Protocol
    """
    
    
    Description = Model.OneElement()
    
    StudySummary = Model.OneElement()
    
    StudyStructure = Model.OneElement()
    
    TrialPhase = Model.OneElement()
    
    StudyTimings = Model.OneElement()
    
    StudyIndications = Model.OneElement()
    
    StudyInterventions = Model.OneElement()
    
    StudyObjectives = Model.OneElement()
    
    StudyEndPoints = Model.OneElement()
    
    StudyTargetPopulation = Model.OneElement()
    
    StudyEstimands = Model.OneElement()
    
    InclusionExclusionCriteria = Model.OneElement()
    
    StudyEventGroupRef = Model.ManyElements()
    
    WorkflowRef = Model.OneElement()
    
    Alias = Model.ManyElements()
    
