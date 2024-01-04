import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyInterventionRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyInterventionRef
    """
    
    StudyInterventionOID = Model.Attribute()
    
    
