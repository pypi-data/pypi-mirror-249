import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class GeoPosition(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/GeoPosition+Element
    """
    
    Longitude = Model.Attribute()
    
    Latitude = Model.Attribute()
    
    Altitude = Model.Attribute()
    
    
