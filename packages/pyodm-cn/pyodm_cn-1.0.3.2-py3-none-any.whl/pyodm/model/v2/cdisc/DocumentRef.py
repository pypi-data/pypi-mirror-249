import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class DocumentRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/DocumentRef
    """
    
    LeafID = Model.Attribute()
    
    
    PDFPageRef = Model.ManyElements()
    
