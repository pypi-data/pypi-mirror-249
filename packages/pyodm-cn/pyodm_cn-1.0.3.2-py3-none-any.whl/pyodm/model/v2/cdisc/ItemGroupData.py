import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ItemGroupData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemGroupData+Element
    """
    
    ItemGroupOID = Model.Attribute()
    
    ItemGroupRepeatKey = Model.Attribute()
    
    TransactionType = Model.Attribute()
    
    ItemGroupDataSeq = Model.Attribute()
    
    
    Query = Model.ManyElements()
    
    ItemGroupData = Model.ManyElements()
    
    ItemData = Model.ManyElements()
    
    AuditRecord = Model.OneElement()
    
    Signature = Model.OneElement()
    
    Annotation = Model.ManyElements()
    
