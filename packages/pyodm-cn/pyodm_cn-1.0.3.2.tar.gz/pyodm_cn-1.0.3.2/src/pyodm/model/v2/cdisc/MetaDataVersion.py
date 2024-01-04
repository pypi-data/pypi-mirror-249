import pyodm.model.definition as Model
import pyodm.model.meta.cdisc_odm_entity as Meta


class MetaDataVersion(Meta.CdiscODMEntity):
    """
    https://wiki.cdisc.org/display/ODM2/MetaDataVersion
    """
    
    OID = Model.Attribute()
    
    Name = Model.Attribute()
    
    CommentOID = Model.Attribute()
    
    
    Description = Model.OneElement()
    
    Include = Model.ManyElements()
    
    Standards = Model.ManyElements()
    
    AnnotatedCRF = Model.ManyElements()
    
    SupplementalDoc = Model.ManyElements()
    
    ValueListDef = Model.ManyElements()
    
    WhereClauseDef = Model.ManyElements()
    
    Protocol = Model.ManyElements()
    
    WorkflowDef = Model.ManyElements()
    
    StudyEventGroupDef = Model.ManyElements()
    
    StudyEventDef = Model.ManyElements()
    
    ItemGroupDef = Model.ManyElements()
    
    ItemDef = Model.ManyElements()
    
    CodeList = Model.ManyElements()
    
    ConditionDef = Model.ManyElements()
    
    MethodDef = Model.ManyElements()
    
    CommentDef = Model.ManyElements()
    
    Leaf = Model.ManyElements()
    
