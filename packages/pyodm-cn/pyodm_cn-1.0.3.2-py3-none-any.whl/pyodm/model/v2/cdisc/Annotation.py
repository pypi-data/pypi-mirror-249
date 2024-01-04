
import pyodm.model.meta.cdisc_odm_entity as Meta
import pyodm.model.definition as Model


class Annotation(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/Annotation
    """
    
    SeqNum = Model.Attribute()
    
    TransactionType = Model.Attribute()
    
    ID = Model.Attribute()

    Comment = Model.OneElement()
    
    Coding = Model.ManyElements()
    
    Flag = Model.ManyElements()
    
