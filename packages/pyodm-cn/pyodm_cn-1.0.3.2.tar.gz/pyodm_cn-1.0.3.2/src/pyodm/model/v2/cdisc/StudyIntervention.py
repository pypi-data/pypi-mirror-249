import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyIntervention(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyIntervention
    """
    
    OID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Coding = Model.ManyElements()
    
