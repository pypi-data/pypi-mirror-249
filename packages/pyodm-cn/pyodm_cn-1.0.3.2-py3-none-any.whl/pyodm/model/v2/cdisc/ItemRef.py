import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class ItemRef(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/ItemRef
    """
    
    ItemOID = Model.Attribute()
    
    KeySequence = Model.Attribute()
    
    IsNonStandard = Model.Attribute()
    
    HasNoData = Model.Attribute()
    
    MethodOID = Model.Attribute()
    
    UnitsItemOID = Model.Attribute()
    
    Repeat = Model.Attribute()
    
    Other = Model.Attribute()
    
    Role = Model.Attribute()
    
    RoleCodeListOID = Model.Attribute()
    
    Core = Model.Attribute()
    
    PreSpecifiedValue = Model.Attribute()
    
    OrderNumber = Model.Attribute()
    
    Mandatory = Model.Attribute()
    
    CollectionExceptionConditionOID = Model.Attribute()
    
    
    Origin = Model.ManyElements()
    
    WhereClauseRef = Model.ManyElements()
    
