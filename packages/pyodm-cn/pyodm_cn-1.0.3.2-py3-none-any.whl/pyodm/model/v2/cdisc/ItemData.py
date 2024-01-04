import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ItemData(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemData+Element
    """
    
    ItemOID = Model.Attribute()
    
    TransactionType = Model.Attribute()

    IsNull = Model.Attribute()

    Value = Model.ManyElements()
    
    Query = Model.ManyElements()

    AuditRecord = Model.ManyElements()

    
