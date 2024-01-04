import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyIndications(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyIndications
    """
    
    
    StudyIndication = Model.ManyElements()
    
