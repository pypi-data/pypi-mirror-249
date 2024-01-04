import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class StudyEndPointRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/StudyEndPointRef
    """
    
    StudyEndPointOID = Model.Attribute()
    
    OrderNumber = Model.Attribute()
    
    
